import hmac
import json
import hashlib

from flask import request, abort
import giturlparse

from github_jenkins_proxy import app, handlers


@app.route('/', methods=['POST'])
def index():
    _check_signature()
    handler = _get_event_handler()
    payload = _get_payload()
    return handler(payload)


@app.route('/jenkins', methods=['POST', 'GET'])
def jenkins_notifications():
    payload = json.loads(request.data)
    _set_pr_status(payload['build'])
    return json.dumps({})


def _set_pr_status(build_info):
    if build_info['phase'] not in ('FINALIZED', 'COMPLETED'):
        return
    if build_info['status'] == 'FAILURE':
        state, description = 'failure', 'Build failed'
    else:
        state, description = 'success', 'Build succeeded'
    job_path = build_info['url']
    # FIXME: Will we get all repo that we are building or what ?
    # detailled_build_info = jenkins.get_build_info(build_info['name'], build_info['build']['number'])

    repo = giturlparse.parse(build_info['scm']['url'])
    sha = build_info['scm']['commit']
    statuses_url = 'https://api.github.com/repos/{owner}/{name}/statuses/{sha}'.format(sha=sha, name=repo.repo, owner=repo.owner)
    app.logger.info('send notification to %s', statuses_url)
    handlers._set_github_status(state, description, job_path, statuses_url)


def _check_signature():
    signature = request.headers.get('X-Hub-Signature')
    if not signature:
        return
    digestmod, signature = signature.split('=')
    try:
        digestmod = getattr(hashlib, digestmod)
    except AttributeError:
        app.logger.error('Unkown disgest method %r', disgestmod)
        abort(501)

    mac = hmac.new(app.config.GITHUB_SIGNATURE_SECRET, msg=request.data, digestmod=digestmod)
    if not hmac.compare_digest(mac.hexdigest(), signature):
        app.logger.warning('signature not matching')
        abort(403)


def _get_event_handler():
    event = request.headers.get('X-GitHub-Event', 'ping')
    try:
        return getattr(handlers, event)
    except AttributeError:
        app.logger.info('unknown event %r', event)
        abort(400)


def _get_payload():
    try:
        return json.loads(request.data)
    except ValueError:
        app.logger.error('malformed json pyload')
        abort(400)
