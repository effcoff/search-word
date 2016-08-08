# search-word
weblioから単語検索して、登録していく  
検索だけとしても利用できる

## 環境
* Python3

## 必要パッケージ
* lxml
* cssselect
* requests
* sqlalchemy

## 使い方
### CUI
python main.py  
で実行  
自分のデータベースを作成した場合  
main.py の74行目のところを好きな名前にかえましょう。  
例：wordSearch = WordSerach('sqlite:///myword.db')

allで登録されている前単語表示

### GUI
  まだ

## 追加予定
### 共通
* 指定した単語を削除  
* 学習機能的なやつを追加

### GUI
* 私の環境では、日本語が表示されなかったので修正  
* 登録してある、単語リストを表示する
