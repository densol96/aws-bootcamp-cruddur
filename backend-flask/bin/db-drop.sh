#! /usr/bin/bash

psql $SERVER_DB_CONNECTION_URL -c "DROP DATABASE IF EXISTS cruddur;"