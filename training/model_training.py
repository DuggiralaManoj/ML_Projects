import os
import shutil
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib
import kagglehub

# Set up directories
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DATASETS_DIR = os.path.join(PROJECT_ROOT, 'datasets')
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')

os.makedirs(DATASETS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

def train_and_save_model(dataset_id, target_column, name_prefix):
    # 1. Download dataset using KaggleHub
    dataset_dir = kagglehub.dataset_download(dataset_id)

    # 2. Find CSV file inside the dataset
    csv_path = None
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if file.endswith('.csv'):
                csv_path = os.path.join(root, file)
                break

    if csv_path is None:
        raise Exception(f"No CSV file found for dataset {dataset_id}")

    # 3. Copy to datasets folder
    dataset_copy_path = os.path.join(DATASETS_DIR, f"{name_prefix}_dataset.csv")
    shutil.copyfile(csv_path, dataset_copy_path)
    print(f" Dataset saved to: {dataset_copy_path}")

    # 4. Load and preprocess data
    df = pd.read_csv(csv_path)

    # Special handling for breast cancer dataset
    # Special handling for breast cancer dataset
    if name_prefix == "breast_cancer":
        if "id" in df.columns:
            df.drop(columns=["id"], inplace=True)

        # 🛠️ Drop unnamed column if present
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Encode diagnosis column (M = 1, B = 0)
        le = LabelEncoder()
        df[target_column] = le.fit_transform(df[target_column])  # M = 1, B = 0

        # Save label encoder
        label_encoder_path = os.path.join(MODELS_DIR, f"{name_prefix}_label_encoder.pkl")
        joblib.dump(le, label_encoder_path)
        print(f"Label encoder saved to: {label_encoder_path}")

    # Split features and label
    X = df.drop(target_column, axis=1)
    y = df[target_column]

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_scaled, y)

    # Save model and scaler
    model_path = os.path.join(MODELS_DIR, f"{name_prefix}_model.pkl")
    scaler_path = os.path.join(MODELS_DIR, f"{name_prefix}_scaler.pkl")

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

    print(f" Model saved to: {model_path}")
    print(f" Scaler saved to: {scaler_path}")
    print(f" Training complete for {name_prefix} ({X.shape[1]} features)\n")

# Train all 3 models
if __name__ == "__main__":
    train_and_save_model('akshaydattatraykhare/diabetes-dataset', 'Outcome', 'diabetes')
    train_and_save_model('yasserh/breast-cancer-dataset', 'diagnosis', 'breast_cancer')
    train_and_save_model('johnsmith88/heart-disease-dataset', 'target', 'heart_disease')
