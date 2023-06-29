@Library('my-shared-library') _

pipeline{
    agent any

    parameters{
        choice(name: 'action', choices: 'create\ndelete', description: 'Choose create/Destroy')
        string(name: 'ImageName', description: 'name of the docker build', defaultValue: 'pythonapp')
        string(name: 'ImageTag', description: 'tag of the docker build', defaultValue: 'v1')
        string(name: 'AppName', description: 'name of the application', defaultValue: 'videoapp')
    }

    stages{

        stage('Git Checkout'){
            
            steps{
                
                gitCheckout(
                    branch: "main",
                    url: "https://github.com/honeysaxena/vapp.git"
                )
            }
        }
        stage('Pytest'){
            

            steps{
                script{
                    pyTest()
                }
            }
        }            
        stage('Static code analysis pylint'){
            

            steps{
                script{
                    staticCodeAnalysis()
                }
            }
        }
        stage('Docker Image Build'){
            

            steps{
                script{
                    dockerBuild("${params.ImageName}","${params.ImageTag}","${params.AppName}")
                }
            }
        }         
            
        
    }
}

