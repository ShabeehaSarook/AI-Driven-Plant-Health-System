import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

DATA_PATH = "data/plant_health_data.csv"
df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print(df.head())

TARGET_COLUMN = "target"

y = df[TARGET_COLUMN]

X = df.drop(columns=[TARGET_COLUMN]).select_dtypes(include=["number"])

print("\nNumeric Features Used:")
print(X.columns.tolist())

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "plant_model.pkl")
joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully at:", MODEL_PATH)
print("\nTraining completed successfully")
