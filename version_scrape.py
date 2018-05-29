#Used for scraping osu version names from osu.ppy.sh and storing them into self database

import urllib.request, json
import MySQLdb
import MySQLdb.cursors
import time, calendar, string
import atexit

with open("config.json", "r") as f:
    config = json.load(f)

with open("memory.json", "r") as f:
    memory = json.load(f)

sql = MySQLdb.connect(**config["sql"], cursorclass = MySQLdb.cursors.DictCursor)

cur = sql.cursor()

def on_close():
    with open("memory.json", "w") as f:
        json.dump(memory, f)
    print("Closing...")

atexit.register(on_close)

#---------------------------------------

VERSIONS = check("_") # Gets all versions
BRANCH = {
	"_": VERSIONS
}
SCAN = string.printable[:62] + "-+.:,"

def check(s):
	return urllib.request.urlopen("https://osu.ppy.sh/web/get-internal-version.php?v={}".format(s)).read().decode()

"""
TMP = ""
def scope(v):
	global TMP
	TMP = ""
	o_key = ""
	o_value = v["_"]
	v = _scope(v)
	print(v)
	print(TMP)
	print(o_key)
	print(o_value)

def _scope(v):
	global TMP
	for key, value in v.items():
		if type(value) is int:
			if len(v) is 1:
				return key
			continue
		TMP += key
		return _scope(v[key])
		

	return {o_key: o_value}

	OUT = ""
	ENTRIES = v["_"]
	for key, value in v.items():
		if key is "_":
			continue
		elif type(value) is int:
			return key
		else:
			S = scope(v[key])
			OUT += key + S.keys()[0]
			ENTRIES = S.values()[0]
	return {OUT: ENTRIES}
"""

char_index = 0
current_string = "_"
while memory["version_scrape"]["last"] < VERSIONS:
	
	
	"""
	
	s = scope(BRANCH)
	if s.endswith("_"): # Branch into?
		entries = BRANCH[s]
		if entries is 0:
			
			continue # Meh... we are at the end
	else:
	"""
			
	#r = check()