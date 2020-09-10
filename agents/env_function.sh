#!/bin/bash
aws lambda update-function-configuration --function-name AgentStatus --environment "Variables={$1}"
