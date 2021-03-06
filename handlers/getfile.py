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

    return callback(method_name, request.args.get(method_name))

def callback(method, data):
    cur = glob.sql.cursor()

    if method is "timestamp":
        cur.execute("SELECT * FROM updates WHERE timestamp <= '{}' ORDER BY timestamp DESC LIMIT 1".format(
            data
        ))
    else:
        query = "SELECT * FROM updates WHERE {} = {} LIMIT 1"
        if method is "file_hash":
            query = "SELECT * FROM updates WHERE {} = '{}' LIMIT 1"
        cur.execute(query.format(
            method,
            data
        ))

    return cur.fetchone()