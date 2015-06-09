github-jenkins-proxy
====================

Example
=======

This repository come with a demo to show how this can be used.

1. Start by configuring webhooks for an github repository.

- https://github.com/<user>/<repo>/settings/hooks

2. Create a configuration file.

3. Check which tunnel was assigned to you by checking logs of ngrok
   ``docker-compose logs ngrok``, e.g. https://5e56ba6.ngrok.com


::

    git clone https://github.com/mouadino/github-jenkins-proxy.git
    docker-compose up


Jenkins plugins
===============

- Multiple SCMs Plugin: https://wiki.jenkins-ci.org/display/JENKINS/Multiple+SCMs+Plugin
- Notification Plugin: https://wiki.jenkins-ci.org/display/JENKINS/Notification+Plugin

TODO
====

- [ ] Show how to configure template job
- [ ] Include basic template job xml in demo
- [ ] Refactor
- [ ] Check PR dependencies
- [ ] Check why stop build doesn't work
