#Used to zip all the files into new local folders after downloader is done

import urllib.request, json
import MySQLdb
import MySQLdb.cursors
import os
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

cur.execute("SELECT file_version,filename,file_hash,url_full FROM updates")
data = cur.fetchall()

# Remove already downloaded files (checked from memory.json)
data = data[memory["zipper"]["last"]:]

# Unfinished - replace with zipper code
"""
for row in data:
	try:
		print("Downloading {} with id {}".format(row["filename"], row["file_version"]))
		urllib.request.urlretrieve(
				row["url_full"],
				os.path.join(
					config["downloader"]["download_folder"],
					row["filename"],
					"f_" + row["file_hash"]
				)
			)
		print("Done.")
	except Exception as e:
		memory["downloader"]["failed"].append(row["file_version"])
		print("Error downloading file {}: {}".format(row["file_version"], e))
	memory["downloader"]["last"] += 1
"""