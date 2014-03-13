from pymongo import MongoClient

client = MongoClient('mongodb://doge:doge@oceanic.mongohq.com:10033/AnonDoge')

db = client['AnonDoge']

msgs = db.msgs

def post(hashed_public_key, encrypted_key, encrypted_msg, signature):

	msg = {
		"to": hashed_public_key,
		'encrypted_key': encrypted_key,
		'encrypted_msg': encrypted_msg,
		'signature': signature
	}
	id = msgs.insert(msg)
	return id

def get(hashed_public_key):

	matches = list(msgs.find({"to": hashed_public_key}))

	for msg in matches:
		del msg['_id']

	msgs.remove({"to": hashed_public_key})

	return matches

def downloaded(msg_id):

	if msgs.find_one({"_id": msg_id}).count() is 0:
		return True
	else:
		return False