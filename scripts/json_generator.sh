#!/bin/bash

i=1
echo "[" >../tv-spain.json

while read s; do

if $(echo $s| cut -d\| -f2 | awk '{print $1}' | grep -iq "http"); then
    echo "{
  \"id\": $i,
  \"enabled\": true,
  \"name\": \"$(echo $s| cut -d\| -f1 | sed 's/ *$//')\",
  \"link_m3u8\": \"$(echo $s| cut -d\| -f2 | sed 's/^ *//')\",
  \"link_logo\": \"\"
}," >> ../tv-spain.json
    
    let i=$i+1
fi

done <<< $(awk '/--- | ---/,EOF' ../README.md  | tail -n +2)


sed -i '$ s/.$//' ../tv-spain.json

echo "]" >>../tv-spain.json
