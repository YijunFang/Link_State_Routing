#!/bin/sh
osascript <<END
tell application "Terminal"
    do script "cd \"`pwd`\";$1"
end tell
END
# you will get FL grade if you can not write this shell  LOL
