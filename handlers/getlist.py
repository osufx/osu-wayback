from objects import glob

allowed_args = ["file_hash", "file_version", "timestamp"]

def handle(request):
    if len([x for x in request.args if x in allowed_args]) == 0:
        return {
                "error": "Missing valid args",
                "allowed": allowed_args
            }

    for i in range(len(allowed_args)): # Gets the first valid argument and sets it as the method handler
        method = request.args.get(allowed_args[i])
        method_name = allowed_args[i]
        if method is not None:
            break

    return callback(method_name)

def callback(method):
    cur = glob.sql.cursor()

    cur.execute("SELECT {} FROM updates WHERE filename = 'osu!.exe' ORDER BY file_version".format(
        method
    ))

    data = []
    for row in cur.fetchall():
        data.append(row[method])

    return data