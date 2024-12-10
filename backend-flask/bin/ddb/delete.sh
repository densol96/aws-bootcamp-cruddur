#!/usr/bin/bash
set -e # stop if it fails at any point

# ./delete.sh dev cruddur-messages

if [ -z "$2" ]; then
    echo "No table name provided. Exiting the process"
    exit 1
fi

if [ "$1" = "prod" ]; then
    ENDPOINT_URL=""
else 
    ENDPOINT_URL="http://localhost:8000"
fi

aws dynamodb delete-table --endpoint-url=$ENDPOINT_URL --table-name $2