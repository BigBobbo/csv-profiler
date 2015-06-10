import datetime

try:
    from ebaysdk.finding import Connection as Finding
except:
    import pip
    pip.main(['install', '--user', 'ebaysdk'])
    from ebaysdk.finding import Connection


try:
    api = Finding(appid=appid, config_file=None)

    response = api.execute('findItemsByProduct', {'productId.type':'ReferenceID', 'productID.value':'311341714658' })
    print(response.dict())
except ConnectionError as e:
    print(e)
    print(e.response.dict())

