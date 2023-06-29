@Library('my-shared-library') _

pipeline{
    agent any

    parameters{
        choice(name: 'action', choices: 'create\ndelete', description: 'Choose create/Destroy')
    }

    stages{

        stage('Git Checkout'){
            when { expression { params.action == 'create '} }
            steps{
                
                gitCheckout(
                    branch: "main",
                    url: "https://github.com/honeysaxena/vapp.git"
                )
            }
        }
        stage('Pytest'){
            
            when { expression { params.action == 'create '} }

            steps{
                script{
                    pyTest()
                }
            }
        }            
        stage('Static code analysis SOnarqube'){
            
            when { expression { params.action == 'create '} }

            steps{
                script{
                    staticCodeAnalysis()
                }
            }
        }        
            
        
    }
}

