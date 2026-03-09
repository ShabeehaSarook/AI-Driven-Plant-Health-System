import os
import json
from datetime import datetime

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

DATA_PATH = "data/plant_health_data.csv"
TARGET_COLUMN = "target"

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "plant_model.pkl")
MODEL_META_PATH = os.path.join(MODEL_DIR, "plant_model.meta.json")

REPORTS_DIR = "reports"


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _timestamp() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def save_confusion_matrix(cm, labels, out_path: str, title: str = "Confusion Matrix"):
    plt.figure(figsize=(7, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.title(title)
    plt.ylabel("True")
    plt.xlabel("Predicted")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def save_feature_importance(model, feature_names, out_path: str, title: str = "Feature Importance"):
    importances = getattr(model, "feature_importances_", None)
    if importances is None:
        return

    fi = (
        pd.DataFrame({"feature": feature_names, "importance": importances})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(data=fi, x="importance", y="feature", orient="h")
    plt.title(title)
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Training data not found: {DATA_PATH}. "
            "Place your CSV at ai-service/data/plant_health_data.csv (or update DATA_PATH)."
        )

    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded successfully")
    print(df.head())

    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in dataset")

    y = df[TARGET_COLUMN]
    X = df.drop(columns=[TARGET_COLUMN]).select_dtypes(include=["number"])

    print("\nNumeric Features Used:")
    print(X.columns.tolist())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

    ts = _timestamp()
    _ensure_dir(MODEL_DIR)
    _ensure_dir(REPORTS_DIR)
    report_txt = classification_report(y_test, y_pred)
    report_dict = classification_report(y_test, y_pred, output_dict=True)

    report_txt_path = os.path.join(REPORTS_DIR, f"classification_report_{ts}.txt")
    with open(report_txt_path, "w", encoding="utf-8") as f:
        f.write(report_txt)

    report_json_path = os.path.join(REPORTS_DIR, f"classification_report_{ts}.json")
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(report_dict, f, indent=2)

    print("\nClassification Report saved:")
    print("-", report_txt_path)
    labels = sorted(list(pd.unique(y)))
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    cm_path = os.path.join(REPORTS_DIR, f"confusion_matrix_{ts}.png")
    save_confusion_matrix(cm, labels, cm_path)
    fi_path = os.path.join(REPORTS_DIR, f"feature_importance_{ts}.png")
    save_feature_importance(model, X.columns.tolist(), fi_path)
    summary = {
        "timestamp_utc": ts,
        "data_path": DATA_PATH,
        "n_samples": int(df.shape[0]),
        "n_features": int(X.shape[1]),
        "feature_names": X.columns.tolist(),
        "model": {
            "type": "RandomForestClassifier",
            "params": model.get_params(),
        },
        "metrics": {
            "accuracy": float(accuracy),
            "accuracy_percent": float(round(accuracy * 100, 2)),
        },
        "artifacts": {
            "classification_report_txt": report_txt_path,
            "classification_report_json": report_json_path,
            "confusion_matrix_png": cm_path,
            "feature_importance_png": fi_path,
        },
    }

    summary_path = os.path.join(REPORTS_DIR, f"training_summary_{ts}.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    joblib.dump(model, MODEL_PATH)
    model_meta = {
        "model_path": MODEL_PATH,
        "trained_at_utc": ts,
        "model_version": f"rf_{ts}",
        "algorithm": "RandomForestClassifier",
        "n_features": int(X.shape[1]),
        "feature_names": X.columns.tolist(),
        "metrics": {"accuracy": float(accuracy), "accuracy_percent": float(round(accuracy * 100, 2))},
    }
    with open(MODEL_META_PATH, "w", encoding="utf-8") as f:
        json.dump(model_meta, f, indent=2)

    print("\nArtifacts saved to:", REPORTS_DIR)
    print("-", cm_path)
    print("-", fi_path)
    print("-", summary_path)

    print("\nModel saved successfully at:", MODEL_PATH)
    print("\nTraining completed successfully")


if __name__ == "__main__":
    main()
