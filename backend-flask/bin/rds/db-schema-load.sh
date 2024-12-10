#! /usr/bin/bash

schema_path="/workspace/aws-bootcamp-cruddur/backend-flask/db/schema.sql"

if [ "$1" = "dev" ]; then
 psql $CRUDDUR_DB_CONNECTION_URL < $schema_path
else
 psql $AWS_RDS_CONNECTION_URL < $schema_path   
fi