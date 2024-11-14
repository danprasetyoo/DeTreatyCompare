pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'danprasetyoo/comparetify'
        DOCKER_TAG = "${DOCKER_IMAGE}:1.0-${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = 'https://hub.docker.com/repository/docker/danprasetyoo/comparetify/general'
        DEPLOY_ENV = 'production'
    }

    stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    if (fileExists('comparetify-config/docker-compose-test.yml')) {
                        sh 'echo $PASSWORD | sudo -S docker-compose -f comparetify-config/docker-compose-test.yml up --build'
                    } else {
                        echo 'Test file docker-compose-test.yml not found, skipping tests.'
                    }
                }
            }
        }
        
    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh "sudo docker build -t ${DOCKER_TAG} -f comparetify-backend/Dockerfile ."
                }
            }
        }
        
        
        stage('Push to Docker Registry') {
            when {
                branch 'master'
            }
            steps {
                script {
                    echo 'Pushing to Docker Registry...'
                    sh "sudo -S docker tag ${DOCKER_TAG} ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                    sh "sudo -S docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying...'
                    sh 'echo $PASSWORD | sudo -S docker-compose -f comparetify-config/docker-compose.yml up build -d'
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up test containers...'
            script {
                if (fileExists('comparetify-config/docker-compose-test.yml')) {
                    sh 'sudo -S docker-compose -f comparetify-config/docker-compose-test.yml down'
                }
            }
        }
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}
