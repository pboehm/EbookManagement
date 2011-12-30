#!/bin/bash
#
# Script, welches durch incron aufgerufen wird, wenn
# Änderungen in den Ebook-Verzeichnissen auftreten
#
WAIT=10
echo "Warte $WAIT Sekunden"
sleep $WAIT

echo "Starte Update"
cd /usr/local/django/EbookManagement/
./manage.py updatebookindex
