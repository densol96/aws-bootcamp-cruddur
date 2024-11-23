#! /usr/bin/bash
set -e # stop if it fails at any point

bin_path="/workspace/aws-bootcamp-cruddur/backend-flask/bin"
source "$bin_path/db-drop.sh"
source "$bin_path/db-create.sh"
source "$bin_path/db-schema-load.sh"
source "$bin_path/db-seed.sh"
# source "$bin_path/db/update_cognito_user_ids"