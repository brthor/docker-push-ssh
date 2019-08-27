# docker-push-ssh
[![PyPI version](https://badge.fury.io/py/docker-push-ssh.svg)](https://pypi.org/project/docker-push-ssh)
[![Build Status](https://travis-ci.org/brthor/docker-push-ssh.svg?branch=master)](https://travis-ci.org/brthor/docker-push-ssh)

Push docker images from your local machine to remote servers without the hassle.

## Overview
`docker-push-ssh` is a command line utility to push docker images from your local machine to your remote machine via ssh.

It creates a private docker registry on your server, establishes a ssh tunnel (so the registry is never exposed to the public),
and uploads your docker image over this ssh tunnel.

Tested on OS X with "Docker for Mac".

## Install

1. Install via pip:
`pip install docker-push-ssh`

2. Add `localhost:5000` to your docker client's insecure registries (requires restart of docker):

[[OS X] How to Add Insecure Registry](https://stackoverflow.com/questions/32808215/where-to-set-the-insecure-registry-flag-on-mac-os)

[[Linux] How to Add Insecure Registry](https://stackoverflow.com/questions/42211380/add-insecure-registry-to-docker)


Adding `localhost:5000` to your client's insecure registries is inconvenient but a side-effect of docker's design.
It only needs to be done once from each machine using `docker-push-ssh`. This allows the tool to push through the ssh
tunnel at `localhost:5000` to the temporary registry on your remote host, without needing ssl certificates for your server.

## Usage:

```bash
$ docker-push-ssh --help
usage: docker-push-ssh [-h] [-i SSH_IDENTITY_FILE] [-p SSH_PORT]
              ssh_host docker_image [docker_image ...]

A utility to securely push a docker image from your local host to a remote
host over ssh without using docker save/load or needing to setup a private
registry.

positional arguments:
  ssh_host              Host to push docker image to. (ex.
                        username@myhost.com)
  docker_image          Docker image tag(s) to push. Specify one or more
                        separated by spaces.

optional arguments:
  -h, --help            show this help message and exit
  -i SSH_IDENTITY_FILE, --ssh-identity-file SSH_IDENTITY_FILE
                        [required] Path to the ssh identity file on your local
                        host. Required, password auth not supported.
  -p SSH_PORT, --ssh-port SSH_PORT
                        [optional] Port on ssh host to connect to. (Default is
                        22)
  -r REGISTRY_PORT, --registry-port REGISTRY_PORT
                        [optional] Remote registry port on ssh host to forward
                        to. (Default is 5000)
```

## Examples

First create a test image we can use:
```bash
$ mkdir /tmp/testimage && cd /tmp/testimage
$ echo "FROM alpine" >> ./Dockerfile
$ echo "RUN touch /etc/testimage" >> ./Dockerfile
$ docker build -t testimage .
```

Now push that test image to our remote server:
```bash
$ docker-push-ssh -i ~/my_identity_file root@myserver.com testimage
...
```

Now the `testimage` will be present on your server.

## Caveats

1. SSH password authentication is not supported. Only key files.
