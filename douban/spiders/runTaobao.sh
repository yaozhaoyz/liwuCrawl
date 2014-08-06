#! /bin/sh

rm -fr test.*
cur_dir=$(cd "$(dirname "$0")"; pwd)
cd $cur_dir

echo "Begin taobao crawler"
date

echo "cur_dir:$cur_dir"

/usr/local/bin/scrapy crawl taobao --logfile=taobao.log -o taobao.json -t json 1> t1 2> t2

date
echo "Finish taobao crawler\n"

cd -


