# docker-entrypoint.sh
#!/bin/bash

FILE=data/db/test.db
if [ ! -f $FILE ]; then
    sqlite3 -init schema.sql data/db/test.db
fi

python app.py