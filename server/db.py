from pymongo import MongoClient

import config

client = MongoClient(config.database)

db = client['AnonDoge']

msgs = db.msgs
aliases = db.aliases

def get_one():

	msg = msgs.find_one()
	if not msg:
		msg = {'msg': 'Any message up here'}
	else:
		del msg['_id']
	return msg

def get_alias(alias):

	pubkey = aliases.find_one({"alias": alias})
	if pubkey:
		aliases.remove({"alias": alias})
		return pubkey['pubkey']
	else:
		return False

def save_alias(alias, pubkey):

	if aliases.find({"alias": alias}).count() is 0:
		aliases.insert({'alias': alias, 'pubkey': pubkey})
		return True
	else:
		return False

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