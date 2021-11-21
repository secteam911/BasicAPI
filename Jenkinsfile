pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:3.8.5'
                }
            }
            steps {
                withEnv(["HOME=${env.VIRTUAL_VENV}"]) {
                    sh 'pip install -r related.txt'
                    sh 'python app.py initdb'
                    sh 'python app.py runserver'
                }
            }
            post {
                always {
                    junit 'output.xml'
                }
            }
        }
    }
}