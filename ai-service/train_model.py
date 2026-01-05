# ==========================================
# AI-Driven Smart Plant Health System
# Model Training Script
# ==========================================

import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ===============================
# 1. Load Dataset
# ===============================
DATA_PATH = "data/plant_health_data.csv"
df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print(df.head())

# ===============================
# 2. Define Target Column
# ===============================
TARGET_COLUMN = "target"

# ===============================
# 3. Separate Features & Target
# ===============================
y = df[TARGET_COLUMN]

# 🔥 VERY IMPORTANT FIX:
# Keep ONLY numeric columns for ML
X = df.drop(columns=[TARGET_COLUMN]).select_dtypes(include=["number"])

print("\nNumeric Features Used:")
print(X.columns.tolist())

# ===============================
# 4. Train-Test Split
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ===============================
# 5. Train Random Forest Model
# ===============================
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# ===============================
# 6. Evaluate Model
# ===============================
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ===============================
# 7. Save Model
# ===============================
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "plant_model.pkl")
joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully at:", MODEL_PATH)
print("\n🎉 STEP 5 COMPLETED SUCCESSFULLY 🎉")
