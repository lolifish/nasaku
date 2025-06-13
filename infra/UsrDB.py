from datetime import datetime
import sqlite3
import json

from models.UsrData import UsrData

dbpath = "./data/db/usr.db"
timeformat = "%Y-%m-%d"

conn = sqlite3.connect(dbpath)
cur = conn.cursor()

class UsrDB():

	def create(self, id:int):
		cur.execute("INSERT INTO base (id) VALUES (?)", (id, ))
		conn.commit()

	# 获取用户数据
	def get(self, id:int) -> UsrData:
		cur.execute("SELECT id,imp,fish,signin,inventory,chat FROM base WHERE id=?", (id, ))
		d = cur.fetchone()
		if not d:
			return None
		else:
			data = UsrData()

			data.id = d[0]
			data.imp = d[1]
			data.fish = d[2]
			data.signin = datetime.strptime(d[3], timeformat).date()
			data.inventory = json.loads(d[4])
			data.chat = json.loads(d[5])

			return data
	
	# 保存用户数据
	def save(self, data: UsrData):
		d = {
			"imp": data.imp,
			"fish": data.fish,
			"signin": datetime.strftime(data.signin, timeformat),
			"chat": json.dumps(data.chat),
			"inventory": json.dumps(data.inventory)
		}
		for key, value in d.items():
			cur.execute(f'UPDATE base SET {key} =? WHERE id =?', (value, data.id))
	
	# 提交并关闭Cursor
	def commit(self):
		conn.commit()

if __name__ == "__main__":
	#data = UsrDB().create(2571610591)
	data = UsrDB().get(2571610591)
	print(data.inventory)