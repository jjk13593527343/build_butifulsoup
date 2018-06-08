#!/bin/bash

function usage()
{
echo "Usage: sh start.sh saic_crawler.py saic_crawl 10"
}

py_exe="/usr/bin/python"
env="dev"
conf_dir="conf/$env"

if [ ! -f "$1" ]; then
echo "$1 not exists"
usage
fi

jobsrc="$conf_dir/$2.py"
if [ ! -f "$jobsrc" ]; then
echo "$jobsrc not exists."
usage
fi

declare -i i=1
while((i <= $3))
do
job="$2_$i"
cp "$jobsrc" "$conf_dir/$job.py"
#$py_exe $1 $job -e $env
 nohup $py_exe $1 $job -e $env >/dev/null 2>&1 &

pid=`ps gaux | grep $job | grep -v grep | awk '{print $2}'`
echo "$i - $pid"

let ++i
done
