'''第7章: データベース
artist.json.gzは，オープンな音楽データベースMusicBrainzの中で，アーティストに関するものをJSON形式に変換し，gzip形式で圧縮したファイルである．このファイルには，1アーティストに関する情報が1行にJSON形式で格納されている．JSON形式の概要は以下の通りである．

60. KVSの構築
Key-Value-Store (KVS) を用い，アーティスト名（name）から活動場所（area）を検索するためのデータベースを構築せよ．'''

import json
import leveldb
import gzip

fname = 'artist.json.gz'
fname_db = 'test_db'

db = leveldb.LevelDB(fname_db)

with gzip.open(fname, 'rt') as data_file:
  for line in data_file:
    data_json = json.loads(line)

    key = data_json['name'] + '\t' + str(data_json['id'])
    value = data_json.get('area', '')
    db.Put(key.encode(), value.encode())

print('{}件登録しました。'.format(len(list(db.RangeIter(include_value=False)))))