awk -F ';' '{b=""; for(i=1;i<=NF;i++){split($i,a,"=");b=b"\""a[1]"\":\""a[2]"\",";} print b;}' 3
