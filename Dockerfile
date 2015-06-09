FROM ubuntu:latest

MAINTAINER "Mouad Benchchaoui"

ADD . /github_jenkins_proxy

RUN apt-get update
RUN apt-get install --yes python-pip git-core python-dev
RUN pip install -e /github_jenkins_proxy

WORKDIR /github_jenkins_proxy

CMD github_jenkins_proxy/runserver.py
