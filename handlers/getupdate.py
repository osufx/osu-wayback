from objects import glob

allowed_args = ["file_hash", "file_version", "timestamp"]

def handle(request):
    if len([x for x in request.args if x in allowed_args]) == 0:
        return {"error": "Missing valid args"}

    for i in range(len(allowed_args)): # Gets the first valid argument and sets it as the method handler
        method = request.args.get(allowed_args[i])
        method_name = allowed_args[i]
        if method is not None:
            break

    output = {
        "method": method_name,
        "response": callback(method_name, request.args.get(method_name))
    }
    return output

def callback(method, data):
    cur = glob.sql.cursor()

    query = "SELECT a.* FROM updates a INNER JOIN ( SELECT MAX(file_version) file_version, filename FROM updates WHERE {} < {} GROUP BY filename) b ON a.file_version = b.file_version"
    if method is "timestamp":
        query += " ORDER BY a.timestamp DESC"
    elif method is "file_hash":
        query = "SELECT * FROM updates WHERE {} = '{}'"

    cur.execute("SELECT a.* FROM updates a INNER JOIN ( SELECT MAX(file_version) file_version, filename FROM updates WHERE {} < {} GROUP BY filename) b ON a.file_version = b.file_version;".format(
        method,
        data
    ))

    return cur.fetchall()