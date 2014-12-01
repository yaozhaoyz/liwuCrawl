#! /bin/sh

rm -fr test.*
cur_dir=$(cd "$(dirname "$0")"; pwd)
cd $cur_dir

echo "Begin jd crawler"
cd /root/install/scrapy/scrapy/douban/douban/spiders
date

echo "cur_dir:$cur_dir"

/usr/local/bin/scrapy crawl jd --logfile=jd.log -o jd.json -t json 1> t1 2> t2

date
echo "Finish jd crawler\n"

cd -


