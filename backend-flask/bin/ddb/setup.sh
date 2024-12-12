#! /usr/bin/bash
set -e # stop if it fails at any point

bin_path="/workspace/aws-bootcamp-cruddur/backend-flask/bin/ddb"

echo "Setting up dynamodb for $1 environment..."

if [ "$1" = "dev" ]; then
    $bin_path/delete.sh dev cruddur-messages
    $bin_path/schema-load.py
    $bin_path/list-tables.sh
    $bin_path/seed.py
    $bin_path/scan.py
else
    echo "Prod option is not avaialable yet"
    # source "$bin_path/db-drop.sh" prod
    # source "$bin_path/db-create.sh" prod
    # source "$bin_path/db-schema-load.sh" prod
    # source "$bin_path/db-seed.sh" prod
fi

# source "$bin_path/db/update_cognito_user_ids"