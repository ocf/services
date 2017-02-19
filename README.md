# services

[![Build Status](https://jenkins.ocf.berkeley.edu/buildStatus/icon?job=services/master)](https://jenkins.ocf.berkeley.edu/job/services/job/master/)

OCF Marathon service definitions, which are deployed with Jenkins when values
are changed in the app definitions. Apps should have their configuration
changed in this repo instead of through the Marathon web UI, unless the change
is very temporary, because otherwise their changes will be overwritten next
time this repo is deployed.

If the version of a service is not specified in the app definition, it will use
whatever version it is currently deployed with, otherwise the version will be
'pinned', and will set the service to the version specified on every deploy.

## Commands

### To check what has changed

    make diff

### Deploying the new definition changes

    make deploy
