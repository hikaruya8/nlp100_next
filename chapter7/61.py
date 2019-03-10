'''60で構築したデータベースを用い，特定の（指定された）アーティストの活動場所を取得せよ'''

import re
import leveldb

fname_db = 'test_db'

pattern = re.compile(r'''
    ^
    (.*)    # name
    \t      # 区切り
    (\d+)   # id
    $
    ''',re.X + re.DOTALL)

db = leveldb.LevelDB(fname_db)

clue = input("アーティスト名を入力してください")
hit = False

for key, value in db.RangeIter(key_from=(clue + '\t').encode()):
  match = pattern.match(key.decode())
  name = match.group(1)
  id = match.group(2)

  if name != clue:
    break

  area = value.decode()
  if area != '':
    print('{}(id:{})の活動場所:{}'.format(name, id, area))

  else:
    print('{}(id:{})の活動場所は登録されていません'.format(name, id, area))
  hit = True

if not hit:
  print('{}は登録されていません'.format(clue))
