#! /usr/bin/bash
## Example: ENV_VAR = prod
if [ -z "$ENV_VAR" ]; then
  echo "Error: ENV_VAR is not set. Please set it to 'dev' or 'prod'."
  exit 1
fi


case "$ENV_VAR" in
  dev)
    echo "Connecting to docker psql."
    CONNECTION_URL="$CRUDDUR_DB_CONNECTION_URL"
    ;;
  prod)
    echo "Connecting to AWS RDS."
    CONNECTION_URL="$AWS_RDS_CONNECTION_URL"
    ;;
  *)
    echo "Error: Unrecognized ENV_VAR value '$ENV_VAR'. Use 'dev', 'staging', or 'prod'."
    exit 1
    ;;
esac

psql $CONNECTION_URL

