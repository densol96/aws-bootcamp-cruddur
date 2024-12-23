#! /usr/bin/bash
set -e # stop if it fails at any point

bin_path="/workspace/aws-bootcamp-cruddur/backend-flask/bin/sql_db"

echo "Setting up database for $1 environment..."

if [ "$1" = "dev" ]; then
    source "$bin_path/db-drop.sh" dev
    source "$bin_path/db-create.sh" dev
    source "$bin_path/db-schema-load.sh" dev
    source "$bin_path/db-seed.sh" dev
else
    source "$bin_path/db-drop.sh" prod
    source "$bin_path/db-create.sh" prod
    source "$bin_path/db-schema-load.sh" prod
    source "$bin_path/db-seed.sh" prod
fi
python3 "$bin_path/update-cognito-ids.py"
# source "$bin_path/db/update_cognito_user_ids"