# coding:utf-8

"""
テキストファイルに書かれた英単語の意味を調べてCSVファイルに出力する。
英単語暗記アプリ「SmartCard」用。
"""

import codecs
import sys

from bs4 import BeautifulSoup

import requests

###############################################################################
# 変数
###############################################################################
_help = """
[usage] makecsv.py <input> <output>
        <input> : Specify search word text.
        <output> : Specify output CSV file.
"""

###############################################################################
# 関数
###############################################################################


def inputWords(input_path):
    """
    input_path のテキストファイルから単語を読み、そのリストを返す。
    一行一単語を記述すること。
    """
    try:
        with codecs.open(input_path, 'r') as f:
            words = [line.rstrip() for line in f if line.rstrip()]
    except Exception as err:
        print(err)
        print('[Error] Failed to open input file.')
    print('words : {0}'.format(words))
    return words


def translate(word):
    """
    word に格納された単語を翻訳し、意味を文字列で返す。
    意味は https://ejje.weblio.jp から調べる。
    """
    # Search for word meaning
    word_html = requests.get('https://ejje.weblio.jp/content/{0}'.format(word))
    soup = BeautifulSoup(word_html.text, "html.parser")
    metas = soup.find_all('meta')
    for c in metas:
        # print(metas)
        if 'name' in c.attrs and \
           c['name'] == 'twitter:description':
            # 余計な日本語をカットする
            w = c['content'].lstrip('{0}の意味や和訳。'
                                    .format(word)).rstrip('1033万語収録！weblio辞書で英語学習')
            return w
    pass


def outputCSV(words, out_path):
    """
    words に格納された単語を翻訳し、単語とその意味をcsv形式で書き出す。
    一行一単語で出力する
    """
    output = []
    print('Searching...')
    for word in words:
        # 単語の意味を取得
        meaning = translate(word)
        if not meaning:
            print('[Warning] Could not find the meaning of "{0}".'
                  .format(word))
        else:
            # "," を一行に二つ以上書くとダメらしいので置き換える
            output.append(word + ',' + meaning.replace(',','.'))

    # 単語と意味をファイルに出力
    # 文字化けは codecs.open で防げるらしぃ
    print('Output file start.')
    try:
        with codecs.open(out_path, 'w', 'utf-8') as f:
            f.write('\n'.join(output))
        print('Output file succeeded.')
    except Exception as err:
        print("[Error] {0}".format(err))
        print("Failed to write file.")


if __name__ == '__main__':
    argv = sys.argv[1:]
    argc = len(argv)
    if argc != 2:
        print(_help)
        sys.exit(0)

    # Input search words
    search_words = inputWords(argv[0])

    # Output CSV
    out_path = argv[1]
    outputCSV(search_words, out_path)
