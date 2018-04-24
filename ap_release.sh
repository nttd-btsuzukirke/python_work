#!/bin/bash


# バッチサーバ設定ファイル
CURRENT_DIR=`dirname $0`
#. ${CURRENT_DIR}/conf/batchenv.ini

today=$(date "+%Y%m%d")

tag=01
pf=core

work_path="/c/wrk/${today}${tag}_${pf}"

echo ${work_path}

<< comment
mkdir /c/wrk/${today}${tag}_core

cd /c/wrk/2018042403_core

pwd

git clone https://nttd-btsuzukirke@github.com/fastretailing/fr-oms-core-batch.git
#input pass

cd fr-oms-core-batch


pwd


git branch -a


git checkout develop-sandbox5


git merge --no-commit origin/master-sandbox

if confict
git status
-
git diff
git add .
git commit -m "【コメント】"
git status
fi

#check file
pom
application-dev.yml

if [[ modified ]]; then
 	#statements
	git status
	git diff
	git add .
	git status
	git commit -m "【コメント】"
	git status
 
elif [[ no modification ]]; then
	#statements
	git status
	git commit
	git status
	git log

fi

DML
DDL

git push origin develop-sandbox5

comment
