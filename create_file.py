#! python3
# coding: UTF-8

import os


def write_texts(content, file_path, file_name):

    # 結果を入れるディレクトリ作成
    if not os.path.exists(file_path):  # フルパスを指定
        os.makedirs(file_path)  # 再帰的作成
    # ファイル開く
    file = open(file_path + '/' + file_name, 'w')  # ファイルまでのフルパス
    # 記入
    file.write(content)
    file.close()
    return file
