@Library('my-shared-library') _

pipeline{
    agent any

    parameters{
        choice(name: 'action', choices: 'create\ndelete', description: 'Choose create/Destroy')
    }

    stages{

        when { expression { param.action == 'create '} }

        stage('Git Checkout'){
            steps{
                
                gitCheckout(
                    branch: "main",
                    url: "https://github.com/honeysaxena/vapp.git"
                )
            }
        }
        stage('Pytest'){
            
            when { expression { param.action == 'create '} }

            steps{
                script{
                    pyTest()
                }
            }
        }            
        stage('Static code analysis SOnarqube'){
            
            when { expression { param.action == 'create '} }

            steps{
                script{
                    staticCodeAnalysis()
                }
            }
        }        
            
        
    }
}

