'''62. KVS内の反復処理
60で構築したデータベースを用い，活動場所が「Japan」となっているアーティスト数を求めよ'''

import leveldb

fname_db = 'test_db'

db = leveldb.LevelDB(fname_db)

clue = 'Japan'.encode()
result = [value[0].decode() for value in db.RangeIter() if value[1] == clue]

print('{}件'.format(len(result)))