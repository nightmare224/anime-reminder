#!/bin/sh
export PGPASSWORD=$POSTGRES_PASSWORD
createdb animereminder -U postgres
createdb keycloak -U postgres