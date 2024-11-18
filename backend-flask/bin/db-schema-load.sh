#! /usr/bin/bash

schema_path="/workspace/aws-bootcamp-cruddur/backend-flask/db/schema.sql"
psql $CRUDDUR_DB_CONNECTION_URL < $schema_path