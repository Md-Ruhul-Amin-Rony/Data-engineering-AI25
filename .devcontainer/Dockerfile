FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Known, widely-reported devcontainer base-image issue (see e.g.
# https://github.com/devcontainers/features/issues/476 and
# https://github.com/devcontainers/images/issues/1797): this image ships with
# a stale Yarn apt repository (dl.yarnpkg.com) whose GPG key has expired,
# which makes ANY later `apt-get update` fail with NO_PUBKEY 62D54FD4003F6525
# -- including the ones devcontainer Features (docker-in-docker, azure-cli,
# etc.) run internally during their own install scripts. Removing the broken
# repo here, before any Feature runs, fixes it once for all of them.
# We don't need Yarn/Node for this course, so dropping the repo entirely
# (rather than re-signing it) is the simplest correct fix.
RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && rm -f /etc/apt/sources.list.d/yarn.list.save \
    && apt-get update
