#Used for scraping osu version names from osu.ppy.sh and storing them into self database

import json
import MySQLdb
import MySQLdb.cursors
import time, calendar, string
import atexit

# Because ppy site is dumb
import requests

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

SCAN = "_" + string.printable[:62] + "-+.:,"
NAMES = []

def check(s):
    o = requests.get("https://osu.ppy.sh/web/get-internal-version.php?v={}".format(s))
    i = int(o.content.decode())
    return i

def scan_line(s):
    global NAMES
    data = {
        "scan": [],
        "items": 0
    }
    items_found = 0
    current_string = s + "_"
    for i in range(1, len(SCAN)):
        r = check(current_string)

        if current_string.endswith("_"):
            data["items"] = r
            if r is 0: # We hit the end! Add it to the entries list
                c = current_string[:-1]
                print("FOUND: {}".format(c))
                cur.execute("INSERT INTO osu_builds (id,version) VALUES (NULL,%s)", [ c ])
                sql.commit()
                NAMES.append(c)
                break
        elif r > 0: # This is not the length scan and an entry was found so... we add it :D
            print("Pending branch: {} ({} found)".format(current_string, r))
            data["scan"].append(current_string)
            items_found += r

        if items_found >= data["items"]: # We have all the entries for this branch
            print("Found all items in branch: {} ({} found)".format(current_string[:-1], items_found))
            break

        current_string = current_string[:-1] + SCAN[i]
    return data

def branch(s):
    scan_data = scan_line(s)
    for item in scan_data["scan"]:
        branch(item)

branch("") # LEL INIT

for entry in NAMES:
    print(entry)

print("DONE!")