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
            // TODO: right now this just shows the diff and doesn't actually deploy
            sh 'make diff'
        }
    }
}


// vim: ft=groovy
