@Library('my-shared-library') _

pipeline{
    agent any

    parameters{
        choice(name: 'action', choices: 'create\ndelete', description: 'Choose create/Destroy')
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
        //stage('Pytest'){
            

        //    steps{
        //        script{
        //            pyTest()
        //        }
        //    }
        //}            
        stage('Static code analysis SOnarqube'){
            

            steps{
                script{
                    staticCodeAnalysis()
                }
            }
        }        
            
        
    }
}

