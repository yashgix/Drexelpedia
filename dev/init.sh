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

rm -r $DB_NAME
sqlite3 $DB_NAME < $SCRIPT_DIR/db.sql

insert_article 'Towels' "$(cat $SCRIPT_DIR/towels.md)" 42
insert_article 'Drexel Shaft' "$(cat $SCRIPT_DIR/shaft.md)" 27
insert_article 'Drexel CCI' "$(cat $SCRIPT_DIR/cci.md)" 38
insert_article 'Drexel Football Team' "$(cat $SCRIPT_DIR/football.md)" 100

insert_contributor 1 andynines
insert_contributor 1 JohnFry
insert_contributor 1 yashgupta
insert_contributor 2 andynines
insert_contributor 2 yashgupta
insert_contributor 3 stuart
insert_contributor 3 yashgupta
insert_contributor 3 JohnFry
insert_contributor 4 stuart
insert_contributor 4 andynines

echo "DB initialized"
