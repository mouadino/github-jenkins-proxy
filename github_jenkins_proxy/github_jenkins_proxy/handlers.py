import json
import urlparse

import jenkins
import requests

from github_jenkins_proxy import app


jenkins = jenkins.Jenkins(
    app.config['JENKINS_URL'],
    username=app.config['JENKINS_USERNAME'],
    password=app.config['JENKINS_PASSWORD'])


def ping(payload):
    app.logger.debug('ping received hook config is: %r', payload['hook'])
    return json.dumps({'msg': 'pong'})


def pull_request(pr):
    pr_action = pr['action']
    if pr_action in ('opened', 'reopened'):
        on_opened_pull_request(pr['pull_request'])
    elif pr_action == 'closed':
        on_closed_pull_request(pr['pull_request'])
    elif pr_action == 'synchronize':
        on_synchronize_pull_request(pr['pull_request'])
    return json.dumps({})


def on_opened_pull_request(pr_info):
    pr_ref = pr_info['head']['ref']
    if not jenkins.job_exists(pr_ref):
        jenkins.copy_job(app.config['JENKINS_TEMPLATE_JOB'], pr_ref)
    params = job_params_from_pr_info(pr_info)
    jenkins.build_job(pr_ref, params)
    job_info = jenkins.get_job_info(pr_ref)
    job_path = 'job/{0}/{1}/'.format(pr_ref, job_info['nextBuildNumber'])
    _set_github_status('pending', 'Pending job', job_path, pr_info['_links']['statuses']['href'])


def job_params_from_pr_info(pr_info):
    if not app.config['JENKINS_JOB_PARAMETERS']:
        return {}
    pr_number = pr_info['number']
    pr_repo = pr_info['base']['repo']['full_name']
    pr_param = app.config['JENKINS_JOB_PARAMETERS'][pr_repo]
    params = {}
    for param in app.config['JENKINS_JOB_PARAMETERS'].values():
        if param == pr_param:
            params[param] = 'refs/pull/%d/head' % pr_number
        else:
            params[param] = 'refs/heads/master'
    return params


def on_closed_pull_request(pr_info):
    pr_ref = pr_info['head']['ref']
    jenkins.delete_job(pr_ref)


def on_synchronize_pull_request(pr_info):
    pr_ref = pr_info['head']['ref']
    job_info = jenkins.get_job_info(pr_ref)
    # TODO: Remove from queue if it's not building yet !
    # TODO: What happen if job is already done !
    # TODO: Make this stoping build optional !
    # FIXME: Can't stop build fail with MethodNotAllowed !
    # jenkins.stop_build(pr_ref, job_info['nextBuildNumber'] - 1)
    params = job_params_from_pr_info(pr_info)
    jenkins.build_job(pr_ref, params)
    job_path = 'job/{0}/{1}/'.format(pr_ref, job_info['nextBuildNumber'])
    _set_github_status('pending', 'Pending job', job_path, pr_info['_links']['statuses']['href'])


def _set_github_status(state, description, job_path, statuses_url):
    headers = {'Authorization': 'token %s' % app.config['GITHUB_OAUTH_TOKEN']}
    payload = json.dumps({
        'state': state,
        'target_url': urlparse.urljoin(app.config['JENKINS_URL'], job_path),
        'description': description
    })
    requests.post(statuses_url, data=payload, headers=headers)
