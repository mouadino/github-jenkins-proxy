#!/usr/bin/env python
from github_jenkins_proxy import app


if __name__ == '__main__':
    app.run(host='0.0.0.0')
