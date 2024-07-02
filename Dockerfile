# Use the official Miniconda image from the Docker Hub
FROM continuumio/miniconda3

# Set the working directory
WORKDIR /home/mluser/app

# Copy the environment file and install dependencies
COPY conda.yaml .
RUN conda env create -f conda.yaml

# Create a symbolic link to the mlflow command in /usr/bin
RUN ln -s /opt/conda/envs/mlflow_project_env/bin/mlflow /usr/bin/mlflow

# Copy the rest of the working directory contents into the container
COPY . .

# Expose port 5000 for the MLflow tracking server
EXPOSE 5000

CMD mlflow run --backend-config backend_config.json .
