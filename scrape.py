#Used for scraping osu files from osu.ppy.sh and storing them into self database

import urllib.request, json
import MySQLdb
import MySQLdb.cursors
import time, calendar
import atexit

finished = False

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

failed_streak = 0

while not finished:
    target = memory["scrape"]["last"] + 1
    attempts = 0
    completed = False
    extra_sleep = 0
    while attempts < config["scrape"]["max_attempts"] and not completed:
        try:
            with urllib.request.urlopen("https://osu.ppy.sh/web/check-updates.php?action=path&stream=stable&target={}".format(target)) as url:
                data = json.loads(url.read().decode())[0]
                if "url_patch" not in data.keys():
                    data["url_patch"] = None
                cur.execute("INSERT INTO updates (file_version,filename,file_hash,filesize,timestamp,patch_id,url_full,url_patch) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    [
                        data["file_version"],
                        data["filename"],
                        data["file_hash"],
                        data["filesize"],
                        calendar.timegm(time.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")),
                        data["patch_id"],
                        data["url_full"],
                        data["url_patch"]
                    ])
                sql.commit()
                completed = True
                failed_streak = 0
                print("target: {}, status: OK".format(target))
        except:
            if target not in memory["scrape"]["failed"]:
                memory["scrape"]["failed"].append(target)
            attempts += 1
            failed_streak += 1
            if config["scrape"]["increase_delay_on_fail"]:
                extra_sleep = attempts
            print("target: {}, status: FAILED, attempt: {}".format(target, attempts))
        time.sleep(config["scrape"]["delay"] + extra_sleep)
        if failed_streak > 100:
            exit()
    memory["scrape"]["last"] = target