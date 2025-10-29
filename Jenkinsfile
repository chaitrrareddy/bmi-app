pipeline{
    agent any
    stages{
        stage ("Build Docker Image"){
            steps{
                echo "Build Docker Image"
                bat "docker build -t kubeapp:v2 ."
            }
        }
        stage ("Docker Login"){
            steps{
                bat "docker login -u chaitrrareddy -p @Mcr_0205"
            }
        }
        stage("push Docker Iamge to Docker Hub"){
            steps {
                echo "push Docker Image to docker hub"
                bat "docker tag kubeapp:v2 chaitrrareddy/bmi-app:latest"
                bat "docker push chaitrrareddy/bmi-app:latest"


            }
        }
        stage("Deploy to Kubernetes"){
            steps{
                bat "kubectl apply -f deployment.yaml --validate=false"
                bat "kubectl apply -f service.yaml"
            }
        }
    }
    post{
        success{
            echo 'Pipeline completed scucessfull!'

        }
        failure{
            echo "Pipeline failed.Please check the logs."
        }
    }
}
