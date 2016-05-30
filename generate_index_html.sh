#!/bin/sh
#  USAGE: generate_index_html.sh [<title>]
#  DESCRIPTION:
#    This script reads list of index files from the standard input
#    and dumps generated index.html to the stadard output.
#
#    Optionally a title string can be provided.
#
TITLE="$*"

generate_index()
{
_TIMESTAMP="`date`"
# HEAD
cat <<END
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>$TITLE${TITLE:+" - "}$_TIMESTAMP</title>
</head>
<body>
<h1>$TITLE${TITLE:+" - "}$_TIMESTAMP</h1>
<p>This is an automatically generated index file.</p>
END
while read _P
do
    _F=`basename "$_P"`
    echo "<a class=\"index-file\" href=\"$_F\">$_F</a><br />"
done
# FOOT
cat <<END
</body>
</html>
END
}

generate_index