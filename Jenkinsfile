pipeline {
  // TODO: Make this cleaner: https://issues.jenkins-ci.org/browse/JENKINS-42643
  triggers {
    upstream(
      upstreamProjects: (env.BRANCH_NAME == 'master' ? 'ocflib/master' : ''),
      threshold: hudson.model.Result.SUCCESS,
    )
  }

  agent {
    label 'slave'
  }

  options {
    ansiColor('xterm')
    timeout(time: 1, unit: 'HOURS')
    timestamps()
  }

  stages {
    stage('check-gh-trust') {
      steps {
        checkGitHubAccess()
      }
    }

    stage('test') {
      steps {
        sh 'make test'
      }
    }

    stage('deploy-apps') {
      when {
        branch 'master'
      }
      agent {
        label 'deploy'
      }
      steps {
        sh 'make test'
      }
    }
  }

  post {
    failure {
      emailNotification()
    }
    always {
      node(label: 'slave') {
        ircNotification()
      }
    }
  }
}

// vim: ft=groovy
