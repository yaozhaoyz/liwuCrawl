#! /bin/sh

cur_dir=$(cd "$(dirname "$0")"; pwd)
cd $cur_dir

echo "Begin taobao crawler"
date
cd /root/install/scrapy/scrapy/douban/douban/spiders
> tb1
> tb2
> taobao.json
> taobao.log

echo "cur_dir:$cur_dir"

/usr/local/bin/scrapy crawl taobao --logfile=taobao.log -o taobao.json -t json 1> tb1 2> tb2

date
echo "Finish taobao crawler\n"

cd -


