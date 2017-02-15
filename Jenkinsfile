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


// vim: ft=groovy
