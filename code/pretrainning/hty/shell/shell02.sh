#!/bin/bash
function passed() {
    a=$1
    echo "passed(): \$0 is $0"
    echo "passed(): \$1 is $1"
    echo "passed(): \$a is $a"
    echo "passed(): total args is $#"
    echo "passed(): all args (\$@) passed to me - \"$@\""
    echo "passed(): all args (\$*) passed to me - \"$*\""
}

echo "**** calling passed() first time ****"
passed one
echo "**** calling passed() second time ****"
passed one two three
