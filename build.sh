#!/bin/sh

# Get version number
. ./VERSION

# Build lightweight alpine docker image
docker build -t kyubi/yomiko:latest -t kyubi/yomiko:v$VERSION -f Dockerfile.alpine .
