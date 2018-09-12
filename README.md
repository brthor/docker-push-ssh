# docker-push-ssh
Push docker images from your local machine to remote servers without the hassle.

## Overview
`docker-push-ssh` is a command line utility to push docker images from your local machine to your remote machine via ssh.

It creates a private docker registry on your server, establishes a ssh tunnel (so the registry is never exposed to the public),
and uploads your docker image over this ssh tunnel.

Tested on OS X with "Docker for Mac".

## Install

Install via pip:
`pip install docker-push-ssh`

## Usage:

```bash
$ docker-push-ssh --help
usage: docker-push-ssh [-h] [-i SSH_IDENTITY_FILE] [-p SSH_PORT] [-l LOCAL_IP]
              ssh_host docker_image

A utility to securely push a docker image from your local host to a remote
host over ssh without using docker save/load or needing to setup a private
registry.

positional arguments:
  ssh_host              Host to push docker image to. (ex.
                        username@myhost.com)
  docker_image          Docker image name to push.

optional arguments:
  -h, --help            show this help message and exit
  -i SSH_IDENTITY_FILE, --ssh-identity-file SSH_IDENTITY_FILE
                        [required] Path to the ssh identity file on your local
                        host. Required, password auth not supported.
  -p SSH_PORT, --ssh-port SSH_PORT
                        [optional] Port on ssh host to connect to. (Default is
                        22)
  -l LOCAL_IP, --local-ip LOCAL_IP
                        [optional] Ip Address of your local host. Important
                        for systems where docker is run inside a VM (mac,
                        windows). If not provided, a best effort is used to
                        obtain it.
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
2. If you're using any proxy, you'll need to specify `--local-ip` because it probably won't be inferred correctly.