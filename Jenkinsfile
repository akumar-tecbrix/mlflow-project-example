pipeline {
    agent any
    environment {
        DOCKER_CREDENTIALS_ID = 'akumar-dhub'  // Ensure this matches the ID of your Docker Hub credentials in Jenkins
        SPARK_MASTER = 'spark://20.196.27.91:7077'
        MLFLOW_TRACKING_URI = 'http://20.196.27.91:5000'
        DOCKER_IMAGE = 'ajayzkumarz/mlflow-example:v2'
        SWARM_MANAGER_USER = 'azureuser'  // Username for Swarm manager node
        SWARM_MANAGER_HOST = '20.196.27.91'  // IP address of your Swarm manager node
        SSH_CREDENTIALS_ID = 'ssh-docker'  // Jenkins credentials ID for SSH
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}", '.')
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_IMAGE}").push()
                    }
                }
            }
        }

        stage('Deploy to Spark in Docker Swarm') {
            steps {
                script {
                    // Use SSH to run Docker commands on the remote Swarm manager node
                    sshagent (credentials: [SSH_CREDENTIALS_ID]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no ${SWARM_MANAGER_USER}@${SWARM_MANAGER_HOST} 'sudo docker run -d --network host --env MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI} --env SPARK_MASTER=${SPARK_MASTER} ${DOCKER_IMAGE}'
                        """
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
