import io
import sys

from WordSearch import WordSerach

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors='replace')

    wordSearch = WordSerach('sqlite:///word.db')
    line = None
    while True:
        print('< 終了する場合は q を入力してください。 >')
        print('< 検索する言葉を入力してください。 >')
        line = input()
        if line == 'q':
            print('----- 検索終了 -----')
            break
        elif line == 'd':
            while True:
                word = wordSearch.word
                print('< {} を削除しますか？ [t/f] >'.format(word))
                d_line = input()
                if d_line == 't':
                    wordSearch.deleteWord()
                    break
                elif d_line == 'f':
                    break
            continue
        elif line == 'all':
            datas = wordSearch.readAllWord()
            for data in datas:
                print(data[0])
                [print(x) for x in data[1]]
                print('')
            continue

        wordSearch.insertDB(line)
        datas = wordSearch.readWord(line)
        for data in datas:
            print(data)
        word = wordSearch.word
        print('\n< [{}] を削除したい場合は、 d を入力してください。 >'.format(word))
