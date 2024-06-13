# MLflow Project Example

This is a sample MLflow project that demonstrates how to set up a machine learning project using MLflow, containerize it with Docker, and automate the build and deployment process using Jenkins.

## Project Structure

- `Dockerfile`: Defines the Docker image for the project.
- `Jenkinsfile`: Defines the Jenkins pipeline for the project.
- `data/`: Directory for storing data files.
- `mlruns/`: Directory for storing MLflow experiment data.
- `models/`: Directory for storing saved models.
- `requirements.txt`: List of Python dependencies.
- `scripts/`: Directory for storing Python scripts.
- `mlproject`: Defines the MLflow project.
- `.gitignore`: Git ignore file.

## Getting Started

1. Build the Docker image:
   ```bash
   docker build -t mlflow_project_image .
   ```

2. Run the Docker container:
   ```bash
   docker run --rm -v $(pwd):/app mlflow_project_image
   ```

3. Set up Jenkins and configure the pipeline.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
