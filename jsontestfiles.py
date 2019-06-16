import json

symbol = "X"

jsonsymbol = json.dumps(symbol)

notjsonsymbol = json.loads(jsonsymbol)

print(notjsonsymbol)