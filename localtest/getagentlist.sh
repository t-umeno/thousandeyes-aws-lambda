#!/bin/bash
curl https://api.thousandeyes.com/v6/agents.json \
     -u ${THOUSANDEYES_USER}:${THOUSANDEYES_TOKEN}
