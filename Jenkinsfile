if (env.BRANCH_NAME == 'master') {
    properties([
        pipelineTriggers([
            upstream(
                upstreamProjects: 'ocflib/master',
                threshold: hudson.model.Result.SUCCESS,
            ),
        ]),
    ])
}


try {
    node('slave') {
        step([$class: 'WsCleanup'])

        stage('check-out-code') {
            checkout scm
        }

        stage('test') {
            sh 'make test'
        }

        stash 'src'
    }


    if (env.BRANCH_NAME == 'master') {
        node('deploy') {
            step([$class: 'WsCleanup'])
            unstash 'src'

            stage('deploy-apps') {
                sh 'make deploy'
            }
        }
    }

} catch (err) {
    def subject = "${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - Failure!"
    def message = "${env.JOB_NAME} (#${env.BUILD_NUMBER}) failed: ${env.BUILD_URL}"

    if (env.BRANCH_NAME == 'master') {
        slackSend color: '#FF0000', message: message
        mail to: 'root@ocf.berkeley.edu', subject: subject, body: message
    } else {
        mail to: emailextrecipients([
            [$class: 'CulpritsRecipientProvider'],
            [$class: 'DevelopersRecipientProvider']
        ]), subject: subject, body: message
    }

    throw err
}

// vim: ft=groovy
