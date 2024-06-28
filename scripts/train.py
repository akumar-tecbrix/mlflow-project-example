import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Set the name prefix for the run
run_name_prefix = "mlflow_project_example"

# Start an MLflow run
with mlflow.start_run() as run:
    # Set the run name with the prefix
    mlflow.set_tag("mlflow.runName", f"{run_name_prefix}_{run.info.run_id}")

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
