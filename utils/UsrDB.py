from datetime import datetime
import sqlite3
import json

dbpath = "./data/db/usr.db"
timeformat = "%Y-%m-%d"

conn = sqlite3.connect(dbpath)
cur = conn.cursor()

class UsrData():
	id = None
	fish = None
	signin = None
	tags = []
	chat = {}

class UsrDB():

	def create(self, id:int):
		cur.execute("INSERT INTO base (id) VALUES (?)", (id, ))
		conn.commit()

	# 获取用户数据
	def get(self, id:int) -> UsrData:
		cur.execute("SELECT * FROM base WHERE id=?", (id, ))
		d = cur.fetchone()
		if not d:
			return None
		else:
			data = UsrData()

			data.id = d[0]
			data.fish = d[1]
			data.signin = datetime.strptime(d[2], timeformat).date()
			data.tags = json.loads(d[3])
			data.chat = json.loads(d[4])

			return data
	
	# 保存用户数据
	def save(self, data: UsrData):
		d = {
			"fish": data.fish,
			"signin": datetime.strftime(data.signin, timeformat),
			"tags": json.dumps(data.tags),
			"chat": json.dumps(data.chat),
		}
		for key, value in d.items():
			print(key, value)
			cur.execute(f'UPDATE base SET {key} =? WHERE id =?', (value, data.id))
	
	# 提交并关闭Cursor
	def commit(self):
		conn.commit()
