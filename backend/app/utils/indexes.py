"""MongoDB index management.

Indexes are created on startup to ensure correctness and performance.

- users.email unique index prevents duplicate accounts
- predictions compound index improves history queries
"""

from __future__ import annotations

import logging

from pymongo.errors import PyMongoError

from utils.db import users_col, predictions_col

logger = logging.getLogger(__name__)


def ensure_indexes() -> None:
    if users_col is None or predictions_col is None:
        logger.warning("Skipping index creation: database not available")
        return

    try:
        # Unique email for users
        users_col.create_index("email", unique=True, name="uniq_users_email")

        # History query: find by user_id sorted by timestamp desc
        predictions_col.create_index(
            [("user_id", 1), ("timestamp", -1)],
            name="idx_predictions_user_timestamp",
        )

        logger.info("MongoDB indexes ensured")
    except PyMongoError as e:
        # Best-effort: do not crash app startup
        logger.warning("Failed to ensure MongoDB indexes: %s", str(e))
