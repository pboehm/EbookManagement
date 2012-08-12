#!/usr/bin/env bash

# Script that looks for changes in the ebook directories
# through inotifywait. It should run `manage.py updatebookindex` through `a`

if [[ ! -f "settings.py" ]]; then
    echo "You have to 'cd' into the project root"
    exit 1
fi

base_dir=`pwd`

queued_file_flag='/tmp/updatebookindex_has_queued_flag'
test -f $queued_file_flag && rm $queued_file_flag

inotifywait -mr --timefmt '%d/%m/%y %H:%M' --format '%T %w %f' \
-e close_write $@ | while read date time dir file; do

    sleep 1

    if [[ ! -f $queued_file_flag ]]; then
        touch $queued_file_flag
        echo "At ${time} on ${date}, file $FILECHANGE has changed"
        command="rm $queued_file_flag && cd $base_dir && ./manage.py updatebookindex --quiet"
        echo "$command" | at now + 2min
    fi
done
