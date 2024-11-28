#! /usr/bin/bash

if [ "$1" = "dev" ]; then
 CONNECTION_URL="$CRUDDUR_DB_CONNECTION_URL"
else
 CONNECTION_URL="$AWS_RDS_CONNECTION_URL"
fi

psql $CONNECTION_URL -c "CREATE database cruddur;"