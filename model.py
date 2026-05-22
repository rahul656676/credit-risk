import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("dataset.csv")

print(df.columns)

# Encode categorical columns
le = LabelEncoder()

for col in df.select_dtypes(include='object').columns:
    df[col] = le.fit_transform(df[col].astype(str))

# Features & Target
X = df.drop("Risk", axis=1)
y = df["Risk"]

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Model
model = RandomForestClassifier()

# Train
model.fit(X_train, y_train)

# Save Model
joblib.dump(model, "credit_model.pkl")

print("Model Saved Successfully")