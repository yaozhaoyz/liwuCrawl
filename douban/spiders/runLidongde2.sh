#! /bin/sh

rm -fr test.*
cur_dir=$(cd "$(dirname "$0")"; pwd)
cd $cur_dir

echo "Begin lidongde crawler"
date

echo "cur_dir:$cur_dir"

/usr/local/bin/scrapy crawl lidongde2liwu --logfile=test.log -o test.json -t json 1> 1 2> 2

date
echo "Finish lidongde crawler\n"

cd -

#scrapy crawl lidongde --logfile=test.log -o test.json -t json
#scrapy crawl taobao --logfile=test.log -o test.json -t json 1> 1 2> 2

