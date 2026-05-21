# train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

def train():
    # Load dataset
    df = pd.read_csv("disaster_dataset.csv")
    df.columns = df.columns.str.strip()  # this line is for unnecesary spaces in column names


    # Encode categorical columns
    le_disaster = LabelEncoder()
    le_district = LabelEncoder()
    df["disaster_type_enc"] = le_disaster.fit_transform(df["disaster_type"])
    df["district_enc"] = le_district.fit_transform(df["district"])

    # Features and label
    X = df[["disaster_type_enc", "severity", "road_blocked", "district_enc"]]
    y = df["recommended_resources"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print(f"MAE:  {mean_absolute_error(y_test, y_pred):.4f}")
    print(f"R²:   {r2_score(y_test, y_pred):.4f}")

    # Save model and encoders
    joblib.dump(model, "dispatch_model.joblib")
    joblib.dump(le_disaster, "le_disaster.joblib")
    joblib.dump(le_district, "le_district.joblib")
    print("Model and encoders saved.")

if __name__ == "__main__":
    train()