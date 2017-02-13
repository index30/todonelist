# ToDoneList
やった事をまとめるアプリケーション

## Install and Run
```
git clone git@github.com:index30/todonelist.git
./todone.py
```

## Usage
```
./todone.py task_data add
```

タスクの追加  
* タスク名  
* タスクの中身  
* タグ(ex. Python)  

```
./todone.py task_data list
./todone.py task_data list -s (sort_name)
./todone.py task_data list -t (tag_name)
```

タスクの一覧表示  
* -s ... ソートされたタスクの一覧表示(ex. task_idなどを引数にとるとタスクを生成した順(昇順)にソート)  
* -t ... タスクを指定したタグに絞って表示  

```
./todone.py task_data content
./todone.py task_data content -c
./todone.py task_data content -d
```

指定したタスクの詳細表示  
* -c ... 指定したタスクの中身変更  
* -d ... 指定したタスクの削除  
