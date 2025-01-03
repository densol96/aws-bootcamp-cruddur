#!/usr/bin/bash
set -e # stop if it fails at any point

if [ "$1" = "prod" ]; then
    ENDPOINT_URL=""
else 
    ENDPOINT_URL="http://localhost:8000"
fi

aws dynamodb list-tables --endpoint-url=$ENDPOINT_URL --output table