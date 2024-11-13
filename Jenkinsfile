pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'comparetify:1.0'
        DOCKER_REGISTRY = 'https://hub.docker.com/repository/docker/danprasetyoo/comparetify/general' 
        DEPLOY_ENV = 'production' 
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building...'
                    sh 'docker build -t ${DOCKER_IMAGE} .'
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo 'Testing...'
                    sh 'docker-compose -f docker-compose.test.yml up --abort-on-container-exit'
                }
            }
        }
        
        stage('Push to Registry') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo 'Pushing to Docker Registry...'
                    sh 'docker tag ${DOCKER_IMAGE} ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER}'
                    sh 'docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${env.BUILD_NUMBER}'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying...'
                    sh 'docker-compose -f docker-compose.yml up -d'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline complete.'
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
