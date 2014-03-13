import plyvel
import json

db = plyvel.DB('./.db', create_if_missing=True)

def save(subject, receiver, msg, pubkey, privkey):
	db.put(subject,
		json.dumps({
			'msg': msg,
			'receiver': receiver,
			'pubkey': pubkey.decode('utf-8'),
			'privkey': privkey.decode('unicode_escape').encode('utf_8')
		}))

def list():
	arr = list()
	for subject, msg in db:
		msg = json.loads(msg)
		msg['subject'] = subject
		arr.append(msg)

	return arr

def get(subject):
	return json.loads(db.get(subject))

def rename(oldsubject, subject):
	data = db.get(oldsubject)
	batch = db.write_batch()
	batch.put(subject, data)
	batch.delete(oldsubject)
	batch.write()

def delete(subject):
	db.delete(subject)