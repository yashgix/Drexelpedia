#!/bin/bash

set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

DB_NAME="drexelpedia.db"

function insert_article() {
    sqlite3 $DB_NAME "insert into article(title, content, votes) values ('$1', '$2', $3);"
}

function insert_contributor() {
    sqlite3 $DB_NAME "insert into contributor(submission_time, article_id, username) values (strftime('%s') * 1000, '$1', '$2');"
}

insert_article 'Example article' "$(cat $SCRIPT_DIR/example.md)" 0

insert_contributor 5 andynines

echo "DB initialized"
