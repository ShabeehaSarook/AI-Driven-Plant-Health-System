import API from "../services/api";

export async function downloadFile(urlPath, filename = "report.pdf") {
  const res = await API.get(urlPath, { responseType: "blob" });
  const blobUrl = window.URL.createObjectURL(new Blob([res.data]));

  const a = document.createElement("a");
  a.href = blobUrl;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();

  window.URL.revokeObjectURL(blobUrl);
}
