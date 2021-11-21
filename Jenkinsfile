pipeline {
    agent { docker { image 'python:3.8.5' } }
    stages {
        stage('build') {
            steps {
                sh 'pip3 install -r related.txt'
            }
        }
        stage('test') {
            steps {
                sh 'python3 app.py initdb'
		sh 'python3 app.py runserver'
            }
        }
    }
}
