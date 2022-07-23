#!/bin/bash

set -eou pipefail

function check_installed() {
  if [ -z "$(which "$1")" ]
  then
    echo "$1" is not uninstalled
    exit 1
  fi
}

check_installed rsync
check_installed ssh
check_installed scp

if [ -z "$REMOTE_HOST" ]
then
  echo "Need to set \$REMOTE_HOST"
  exit 1
fi

CUR_DIR=$(realpath "$1")
DIR_NAME=$(basename "$CUR_DIR")
if [ ! -d "$CUR_DIR" ]
then
  echo "$CUR_DIR" must be a directory
  exit 1
fi

if [ ! -f "$1/main.tex" ]
then
  echo "$1 doesn't have a main.tex"
  exit 1
fi

HASH=$(shasum <(echo "$CUR_DIR") | cut -f 1 -d ' ')
DEST_DIR="/tmp/$DIR_NAME-$HASH"

echo "Copying files to $REMOTE_HOST"
rsync -a --progress "$1" "$REMOTE_HOST":"$DEST_DIR"

#shellcheck disable=SC2029
ssh "$REMOTE_HOST" "cd $DEST_DIR && latexmk -pdf main"

scp "$REMOTE_HOST:$DEST_DIR/main.pdf" .
