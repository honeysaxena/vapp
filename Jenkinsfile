pipeline{
    agent any

    stages{
        stage('Git Checkout'){
            steps{
                script{
                    git branch: 'h1', url: 'https://github.com/honeysaxena/vapp.git'
                }
            }
        }
    }
}

