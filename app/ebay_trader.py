from ebaysdk.trading import Connection as Trading
try:
HERE
    response = api.execute('GetUser', {})
    print(response.dict())
    print(response.reply)
except ConnectionError as e:
    print(e)
    print(e.response.dict())