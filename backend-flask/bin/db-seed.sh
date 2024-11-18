#! /usr/bin/bash

schema_path="/workspace/aws-bootcamp-cruddur/backend-flask/db/seed.sql"
psql $CRUDDUR_DB_CONNECTION_URL < $schema_path