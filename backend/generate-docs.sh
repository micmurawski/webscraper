#!/usr/bin/env bash

# Don't have aglio installed? Use docker :)
docker run -v ${PWD}:/data christianbladescb/aglio -i /data/docs/api.apib -o /data/templates/docs.html --theme-template triple

# You can use aglio installed locally:
# aglio -i docs/api.apib -o templates/docs.html --theme-template triple
