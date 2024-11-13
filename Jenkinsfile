pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'danprasetyoo/comparetify:1.0'  
        IMAGE_TAG = '1.0'
        DEPLOY_ENV = 'production' 
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'         // Jenkins credentials ID for Docker Hub
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ."
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    sh 'docker-compose -f docker-compose.test.yml up --abort-on-container-exit'
                }
            }
        }
        
        stage('Push to Docker Registry') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo 'Logging into Docker Hub...'
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                    }
                    echo 'Pushing Docker image to registry...'
                    sh "docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                    sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying application...'
                    sh 'docker-compose -f docker-compose.yml up -d'
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up test containers...'
            sh 'docker-compose -f docker-compose.test.yml down'
        }
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}
