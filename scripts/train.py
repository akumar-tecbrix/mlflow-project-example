import mlflow
import mlflow.sklearn
import pandas as pd
import subprocess
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Function to get the current Git commit short hash
def get_git_commit_short_hash():
    try:
        commit_short_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode('utf-8')
        return commit_short_hash
    except Exception as e:
        print(f"Error obtaining Git commit short hash: {e}")
        return None

# Get the Git commit short hash
git_commit_short_hash = get_git_commit_short_hash()

# Set the name prefix for the run
run_name_prefix = "mlflow_project"

# Start an MLflow run
with mlflow.start_run() as run:
    # Set the run name with the prefix
    mlflow.set_tag("mlflow.runName", f"{run_name_prefix}_{run.info.run_id}")

    # Set the Git commit short hash as a tag if available
    if git_commit_short_hash:
        mlflow.set_tag("git_commit_hash", git_commit_short_hash)

    # Load the dataset
    data = pd.read_csv('data/sample_data.csv')
  
    # Split the dataset into training and test sets
    X = data.drop('target', axis=1)
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # Train a RandomForest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    # Make predictions and evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    # Log the model and metrics with MLflow
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "model")
    # Register the model
    model_name = "mlflow_project"
    model_uri = f"runs:/{run.info.run_id}/model"
    
    client = mlflow.tracking.MlflowClient()
    # Check if the model already exists
    try:
        registered_model = client.get_registered_model(model_name)
        print(f"Model {model_name} already exists. Registering a new version.")
    except mlflow.exceptions.RestException:
        # Model does not exist, create it
        print(f"Model {model_name} does not exist. Creating a new model.")
        registered_model = mlflow.register_model(model_uri=model_uri, name=model_name)
    
    # Register a new version of the model
    new_version = client.create_model_version(name=model_name, source=model_uri, run_id=run.info.run_id)

    # Set the Git commit short hash as a tag for the model version if available
    if git_commit_short_hash:
        client.set_model_version_tag(name=model_name, version=new_version.version, key="git_commit_hash", value=git_commit_short_hash)
