# signature when hook is created.
# https://developer.github.com/webhooks/securing/
GITHUB_SIGNATURE_SECRET = ''
# Jenkins endpoint URL.
JENKINS_URL = 'http://jenkins:8080'
# Jenkins username.
JENKINS_USERNAME = None
# Jenkins password.
JENKINS_PASSWORD = None
# Name of jenkins template job.
JENKINS_TEMPLATE_JOB = 'template_job'
# e.g. JENKINS_JOB_PARAMETERS = {'mouadino/github-jenkins-proxy': 'ECHO_REF'}
JENKINS_JOB_PARAMETERS = {}
# GitHub oauth token
# https://help.github.com/articles/creating-an-access-token-for-command-line-use/
GITHUB_OAUTH_TOKEN = ''
# Flask debug flag!
DEBUG = False
