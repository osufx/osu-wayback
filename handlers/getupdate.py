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
        "search_method": method_name
    }
    output["endpoint"] = request.endpoint
    return output