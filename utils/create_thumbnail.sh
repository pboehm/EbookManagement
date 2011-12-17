####
# Script, welches ein Thumbnail von der übergebenen 
# Datei erstellt. 
# Autor: Philipp Böhm
#
# Parameter: 
# 1.) [Pfad zur Quelldatei] 
# 2.) [Pfad zur zu erstellenden Thumbnail-Datei] 
# 3.) [Endung]
#

if [[ $# < 3 ]]
then
    echo "Falsche Parameteranzahl"
    exit 1
fi

SOURCEFILE=$1
TARGETFILE=$2
ENDING=$3

if [[ $ENDING == "pdf" ]]
then
    convert -alpha off -thumbnail x400 "$SOURCEFILE[0]" $TARGETFILE
    exit 0
fi

exit 1