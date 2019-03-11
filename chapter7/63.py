'''63. オブジェクトを値に格納したKVS
KVSを用い，アーティスト名（name）からタグと被タグ数（タグ付けされた回数）のリストを検索するためのデータベースを構築せよ．さらに，ここで構築したデータベースを用い，アーティスト名からタグと被タグ数を検索せよ．'''
import re
import gzip
import json
import leveldb

fname = 'artist.json.gz'
fname_db = 'test_db'

pattern = re.compile(r'''
    ^
    (.*)    # name
    \t      # 区切り
    (\d+)   # id
    $
    ''',re.X + re.DOTALL)


try:
  db = leveldb.LevelDB(fname_db, error_if_exsits=True)

  with gzip.open(fname, 'rt') as data_file:
    for line in data_file:
      data_json = json.loads(line)

      key = data_json['name'] + '\t' + str(data_json['id'])
      value = data_json.get('tags')
      if value is None:
        value = []
      db.Put(key.encode(), json.dumps(value).encode)

     # 確認のため登録件数を表示
    print('{}件登録しました。'.format(len(list(db.RangeIter(include_value=False)))))


except:
  db = leveldb.LevelDB(fname_db)
  print('既存のDBを使う')



# アーティスト名+'\t'で検索
clue = input('アーティスト名を入力する')
hit = False


# アーティスト名+'\t'で検索
for key, value in db.RangeIter(key_from=(clue + '\t').encode()):

  match = pattern.match(key.decode())
  name = match.group(1)
  id = match.group(2)

  if name != clue:
    break

  tags = json.load(value.decode('unicode-escape'))
  print('{}(id:{})のタグ情報):'.format(name,id))
  if len(tags) > 0:
    for tag in tags:
      print('\t{}({})'.format(tag['value'], tag['count']))

  else:
    print('\tタグはありません')
  hit = True


if not hit:
  print('{}は登録されていないです'.format(clue))

