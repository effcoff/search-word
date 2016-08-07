# search-word
weblioから単語検索して、登録していく

-- 必要パッケージ --
・lxml
・requests
・sqlite3

-- 使い方 --
python main.py
で実行
main.py の 114行目のWordSearch()の引数に'mydb.db'などと入力すれば自分用のデータベース作成
例：wordSearch = WordSearch('mydb.db')
