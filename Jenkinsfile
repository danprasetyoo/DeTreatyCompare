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
                    sh "sudo -S docker build -t ${DOCKER_TAG} -f comparetify-backend/Dockerfile comparetify-backend/"
                    sh "sudo -S docker build -t ${DOCKER_TAG} -f comparetify-frontend/Dockerfile comparetify-frontend/"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    if (fileExists('docker-compose-test.yml')) {
                        sh 'sudo -S docker-compose -f docker-compose-test.yml build'
                        // sh 'sudo -S docker-compose -f docker-compose-test.yml up --abort-on-container-exit --exit-code-from backend'
                    } else {
                        echo 'Test file docker-compose-test.yml not found, skipping tests.'
                    }
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
                    sh 'echo $PASSWORD | sudo -S docker-compose -f docker-compose.yml up --build -d'
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up test containers...'
            script {
                if (fileExists('docker-compose-test.yml')) {
                    sh 'sudo -S docker-compose -f docker-compose-test.yml down'
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
