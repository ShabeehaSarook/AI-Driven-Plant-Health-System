import React, { useEffect, useMemo, useState } from "react";
import { getHistory, regenerateReport } from "../services/api";

import { downloadFile } from "../utils/download";

function toLocalDateInputValue(date) {
  // YYYY-MM-DD in local time
  const pad = (n) => String(n).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

function parseIsoDate(value) {
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? null : d;
}

export default function History() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Filters
  const [status, setStatus] = useState("ALL"); // ALL | Healthy | Moderate Stress | High Stress
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [query, setQuery] = useState("");

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const data = await getHistory(200);
        if (mounted) setItems(Array.isArray(data) ? data : []);
      } catch (err) {
        if (mounted) setError(err?.response?.data?.error || "Failed to load history");
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => {
      mounted = false;
    };
  }, []);

  // Default filter values (last 30 days) if empty
  useEffect(() => {
    if (!fromDate && !toDate) {
      const now = new Date();
      const start = new Date();
      start.setDate(now.getDate() - 30);
      setFromDate(toLocalDateInputValue(start));
      setToDate(toLocalDateInputValue(now));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();

    const from = fromDate ? new Date(fromDate + "T00:00:00") : null;
    const to = toDate ? new Date(toDate + "T23:59:59") : null;

    return items.filter((row) => {
      // Status filter
      if (status !== "ALL" && row.prediction !== status) return false;

      // Date range filter
      const ts = row.timestamp ? parseIsoDate(row.timestamp) : null;
      if (from && ts && ts < from) return false;
      if (to && ts && ts > to) return false;

      // Simple search across prediction/confidence
      if (q) {
        const hay = `${row.prediction || ""} ${row.confidence || ""} ${row.confidence_percent ?? ""} ${row.model_version || ""} ${row.timestamp || ""}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }

      return true;
    });
  }, [items, status, fromDate, toDate, query]);

  const clearFilters = () => {
    setStatus("ALL");
    setQuery("");
    setFromDate("");
    setToDate("");
  };

  if (loading) return <div style={{ padding: 16 }}>Loading history...</div>;
  if (error) return <div style={{ padding: 16, color: "crimson" }}>{error}</div>;

  return (
    <div style={{ padding: 16 }}>
      <h2>Prediction History</h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: 12,
          marginBottom: 16,
          padding: 12,
          border: "1px solid #ddd",
          borderRadius: 8,
        }}
      >
        <div>
          <label>Status</label>
          <select style={{ width: "100%" }} value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="ALL">All</option>
            <option value="Healthy">Healthy</option>
            <option value="Moderate Stress">Moderate Stress</option>
            <option value="High Stress">High Stress</option>
          </select>
        </div>

        <div>
          <label>From</label>
          <input style={{ width: "100%" }} type="date" value={fromDate} onChange={(e) => setFromDate(e.target.value)} />
        </div>

        <div>
          <label>To</label>
          <input style={{ width: "100%" }} type="date" value={toDate} onChange={(e) => setToDate(e.target.value)} />
        </div>

        <div>
          <label>Search</label>
          <input
            style={{ width: "100%" }}
            type="text"
            placeholder="Search prediction/confidence/date"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>

        <div style={{ display: "flex", alignItems: "end" }}>
          <button onClick={clearFilters} style={{ width: "100%" }}>
            Clear filters
          </button>
        </div>
      </div>

      <div style={{ marginBottom: 10, color: "#555" }}>
        Showing <strong>{filtered.length}</strong> of <strong>{items.length}</strong> records
      </div>

      {filtered.length === 0 ? (
        <p>No predictions match your filters.</p>
      ) : (
        <div style={{ overflowX: "auto" }}>
          <table border="1" cellPadding="8" style={{ borderCollapse: "collapse", width: "100%" }}>
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Prediction</th>
                <th>Confidence</th>
                <th>Model Version</th>
                <th>Report</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((row) => (
                <tr key={row._id}>
                  <td style={{ whiteSpace: "nowrap" }}>{row.timestamp}</td>
                  <td>{row.prediction}</td>
                  <td>{row.confidence_percent !== undefined && row.confidence_percent !== null ? `${row.confidence_percent}%` : row.confidence}</td>
                  <td style={{ whiteSpace: "nowrap" }}>{row.model_version || "-"}</td>
                  <td>
                    {row.report ? (
                      <button
                        onClick={() => downloadFile(row.report, `plant-health-report-${row._id}.pdf`)}
                        style={{ padding: "4px 10px" }}
                      >
                        Download
                      </button>
                    ) : (
                      "-"
                    )}
                  </td>
                  <td>
                    <button
                      onClick={async () => {
                        try {
                          const res = await regenerateReport(row._id);
                          if (res?.report) {
                            await downloadFile(res.report, `plant-health-report-${row._id}.pdf`);
                          }
                        } catch (e) {
                          // Basic UX: ignore in table; could show toast
                        }
                      }}
                      style={{ padding: "4px 10px" }}
                    >
                      Regenerate
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
