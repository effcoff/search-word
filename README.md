# search-word
weblioから単語検索して、登録していく  
検索だけとしても利用できる

## 環境
* Python3

## 必要パッケージ
### 共通
* lxml
* cssselect
* requests
* sqlalchemy

### GUIの場合
pip installしましょ  
* pyqt5


## 使い方
### CUI
python main.py  
で実行  
自分のデータベースを作成した場合  
main.py の74行目のところを好きな名前にかえましょう。  
例：wordSearch = WordSerach('sqlite:///myword.db')

allで登録されている前単語表示

### GUI
  python gui.pyで実行
  まだ未完成

## 追加予定
### 共通
* 指定した単語を削除  
* 学習機能的なやつを追加

### GUI 
* 登録してある、単語リストを表示する
