pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'danprasetyoo/comparetify'
        DOCKER_TAG = "${DOCKER_IMAGE}:1.0-${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = 'https://hub.docker.com/repository/docker/danprasetyoo/comparetify/general'
        DEPLOY_ENV = 'production'
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh "docker build -t ${DOCKER_TAG} ."
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    if (fileExists('docker-compose.test.yml')) {
                        sh 'docker-compose -f docker-compose.test.yml up --abort-on-container-exit'
                    } else {
                        echo 'Test file docker-compose.test.yml not found, skipping tests.'
                    }
                }
            }
        }
        
        stage('Push to Docker Registry') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo 'Pushing to Docker Registry...'
                    sh "docker tag ${DOCKER_TAG} ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                    sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
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
            echo 'Cleaning up test containers...'
            script {
                if (fileExists('docker-compose.test.yml')) {
                    sh 'docker-compose -f docker-compose.test.yml down'
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
