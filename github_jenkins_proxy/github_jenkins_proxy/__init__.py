from flask import Flask


app = Flask(__name__)
app.config.from_object('github_jenkins_proxy.default_settings')
app.config.from_envvar('GJP_SETTINGS', silent=True)

import github_jenkins_proxy.index
