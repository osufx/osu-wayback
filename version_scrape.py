#Used for scraping osu version names from osu.ppy.sh and storing them into self database

import urllib.request, json
import MySQLdb
import MySQLdb.cursors
import time, calendar
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

URL = "https://osu.ppy.sh/web/get-internal-version.php?v={}"
VERSIONS = urllib.request.urlopen(URL.format("_")) # Gets all versions

BEGINNING = memory["version_scrape"]["last"]
for i in range(VERSIONS):
    pass #Unfinished