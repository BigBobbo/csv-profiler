import datetime

try:
    from ebaysdk.finding import Connection as Finding
except:
    import pip
    pip.main(['install', '--user', 'ebaysdk'])
    from ebaysdk.finding import Connection


try:
    api = Finding(appid="", config_file=None)
    response = api.execute('findItemsAdvanced', {'keywords': "O'Connell Street, Limerick City, Ireland - 1950s ? 4 X 6 Postcard"})
    print(response.dict())
except ConnectionError as e:
    print(e)
    print(e.response.dict())