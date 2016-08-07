# search-word
weblioから単語検索して、登録していく

## 必要パッケージ
* lxml
* requests
* sqlite3

## 使い方
### CUI
python main.py  
で実行  
main.py の 114行目のWordSearch()の引数に'mydb.db'などと入力すれば自分用のデータベース作成  
例：wordSearch = WordSearch('mydb.db')  

allで登録されている前単語表示

### GUI
  まだ

## 追加予定
### 共通
指定した単語を削除  
学習機能的なやつを追加

### GUI
私の環境では、日本語が表示されなかったので修正  
登録してある、単語リストを表示する
