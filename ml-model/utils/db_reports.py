"""DB helpers for report ownership and prediction retrieval."""

from __future__ import annotations

from bson import ObjectId

from utils.db import predictions_col


def get_prediction_by_id(prediction_id: str):
    if predictions_col is None:
        raise Exception("Database not available")
    try:
        oid = ObjectId(str(prediction_id))
    except Exception:
        return None
    return predictions_col.find_one({"_id": oid})


def get_prediction_by_report_path(report_path: str, user_id: str | None = None):
    """Find the prediction record that references a given report path.

    If user_id is provided, the lookup is scoped to that user.
    """
    if predictions_col is None:
        raise Exception("Database not available")

    query = {"report": report_path}
    if user_id:
        query["user_id"] = str(user_id)

    return predictions_col.find_one(query)


def update_prediction_report(prediction_id: str, new_report_path: str):
    if predictions_col is None:
        raise Exception("Database not available")
    try:
        oid = ObjectId(str(prediction_id))
    except Exception:
        return False

    res = predictions_col.update_one({"_id": oid}, {"$set": {"report": new_report_path}})
    return res.modified_count > 0
