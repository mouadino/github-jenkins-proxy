github-jenkins-proxy (PoC)
==========================

Rational
========

I wanted something that manage life cycle of Jenkins job for each Github pull request, the user stories are:

- As a developer when I create a PR I would like to have tests run with my change on all the platform to see if nothing break.
- As a developer when I create a PR I would like to easily see (preferrably like with travis) when tests succeed or fail.
- As a developer when tests of my PR fails I would like to see a snapshot of all logs to figure out what went wrong.
- As a developer I would like to be able to re-run jobs manually and the job output should be reflected in github.
- As a developer I would like to link PRs from different repositories so that a build is run on all dependent PRs.
- As a developer I would like to skip tests for a given PR e.g. for PoC pull request.

How
===

github-jenkins-proxy is a web application that connect Github and Jenkins, it can be configured to receive all notification from Github through Github web hooks (https://developer.github.com/webhooks/) and
then call Jenkins API, what we end up having is:

- For each PR there will be a job specific to it.
- When PR get merged or closed, jenkins job is deleted.
- The job is created from the a template job ``JENKINS_TEMPLATE_JOB`` and can be run by passing parameter to it ``JENKINS_JOB_PARAMETERS``.
- Jenkins can also send notification about job life cycle to proxy which
this later will use to update the github PR status.

Demo
====

This repository come with a demo to show how this can be used.

1. Run demo example (you need for this docker and docker-compose)

```
    git clone https://github.com/mouadino/github-jenkins-proxy.git
    cd github-jenkins-proxy
    docker-compose up
```

2. Check which tunnel was assigned to you by checking logs of ngrok it
should be something like ``https://<some-hash>.ngrok.com``.

3. Configuring webhooks for your github repository, by going to https://github.com/<user>/<repo>/settings/hooks and setting the hooks url to the previous ngrok url.

4. Create a local configuration file in same folder as docker-compose.yml, name it local_settings.py in it you can override
configuration options as specified in github_jenkins_proxy/github_jenkins_proxy/default_settings.py

5. Now go to the jenkins container web interface and create a new job
with same name set in ``JENKINS_TEMPLATE_JOB``.

6. **Optional** Install the Notification Plugin  https://wiki.jenkins-ci.org/display/JENKINS/Notification+Plugin and set
URL to ``https://<some-hash>.ngrok.com/jenkins/``, this will allow the
proxy to receive notification when job start or finish.

Note:
If you want to use notification plugin, you must use the Multiple SCMs Plugin (https://wiki.jenkins-ci.org/display/JENKINS/Multiple+SCMs+Plugin) for managing Jenkins repositories.

TODO
====

- [ ] Include basic template job xml in demo
- [ ] Refactor of course
- [ ] Check PR dependencies
- [ ] Check why stop build doesn't work
