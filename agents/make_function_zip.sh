#!/bin/bash
rm -r v-env
virtualenv --python=python3 v-env
source v-env/bin/activate
pip install boto3
pip install requests
pip install pytz
rm function.zip
(cd $VIRTUAL_ENV/lib/python3.6/site-packages; zip -r9 ${OLDPWD}/function.zip .
)
zip -g function.zip agent_status_lambda.py
deactivate
rm -r v-env
