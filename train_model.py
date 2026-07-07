import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)
# Load dataset
df = pd.read_csv("diabetes_dataset.csv")

# -----------------------------
# Select Features
# -----------------------------
features = [
    "age",
    "bmi",
    "systolic_bp",
    "diastolic_bp",
    "cholesterol_total",
    "glucose_fasting",
    "physical_activity_minutes_per_week"
]

X = df[features]
y = df["diagnosed_diabetes"]

# -----------------------------
# Handle Missing Values
# -----------------------------
X = X.fillna(X.mean())
print(df["diagnosed_diabetes"].unique())
print(df["diagnosed_diabetes"].value_counts())

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# -----------------------------
# Scaling
# -----------------------------
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# -----------------------------
# Train Model
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# Model Evaluation
# -----------------------------

# Predict class labels
pred = model.predict(X_test)

# Predict probabilities
prob = model.predict_proba(X_test)[:, 1]

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, pred)
precision = precision_score(y_test, pred)
recall = recall_score(y_test, pred)
f1 = f1_score(y_test, pred)
roc_auc = roc_auc_score(y_test, prob)
print(f"\nTraining Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")

print("\n========== MODEL EVALUATION ==========\n")

print(f"Accuracy  : {accuracy * 100:.2f}%")
print(f"Precision : {precision * 100:.2f}%")
print(f"Recall    : {recall * 100:.2f}%")
print(f"F1-Score  : {f1 * 100:.2f}%")
print(f"ROC-AUC   : {roc_auc * 100:.2f}%")

print("\nConfusion Matrix")
print(confusion_matrix(y_test, pred))

print("\nClassification Report")
print(classification_report(y_test, pred))
# -----------------------------
# Save Files
# -----------------------------
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("model.pkl saved")
print("scaler.pkl saved")
print(X.columns.tolist())

print("\n========== Feature Importance ==========\n")

importance = model.feature_importances_

for feature, value in sorted(
    zip(features, importance),
    key=lambda x: x[1],
    reverse=True
):
    print(f"{feature:40} {value:.4f}")
    print(df.groupby("diagnosed_diabetes")["physical_activity_minutes_per_week"].mean())