#!/bin/awk -f

BEGIN {
	group = "NONE"
}

/^[A-Z].*/ {
	group = $0
}

/^[ \t]*\[.+\]:/ {
	if(group != "NONE") {
		locale = $1
		gsub(/[\[\]:]/,"",locale)
		printf "msgid \"%s\"\n",group >> "po/"locale".po"
		gsub(/^.*:[ \t]*/,"")
		gsub(/[ \t]*$/,"")
		printf "msgstr \"%s\"\n\n",$0 >> "po/"locale".po"
	}
}
