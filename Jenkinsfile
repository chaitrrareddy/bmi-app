pipeline{
    agent any
    stages {
        stage('Build') {
            steps{
                echo "Build Docker Image"
                bat "docker build -t bmi-app ."
            }
        }
        stage('Run'){
            steps{
                echo "Run application in Docker container"
                bat "docker rm -f mycontainer|| exit 0"
                bat "docker run -d -p 5000:5000 --name myconatiner bmi-app"
            }
        }
    }
    post {
        success{
            echo 'Pipeline completed successfully'
        }
        failure{
            echo 'Pipeline failed. Please check the logs'
        }
    }
}