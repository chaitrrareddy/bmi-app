pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo "🔧 Building Docker Image"
                bat """
                docker build -t bmi-app .
                """
            }
        }

        stage('Run') {
            steps {
                echo "🚀 Running Docker Container"

                // Stop and remove old container if it exists
                bat """
                docker ps -a -q -f name=mycontainer > tmp.txt
                for /f %%i in (tmp.txt) do docker rm -f %%i
                del tmp.txt
                """

                // Run new container
                bat """
                docker run -d -p 5000:5000 --name mycontainer bmi-app
                """
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Please check the logs.'
        }
    }
}
