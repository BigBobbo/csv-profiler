from amazonproduct import API
from test1 import *


import amazonproduct


apiAmazon = API(access_key_id=access_key_id_value,secret_access_key=secret_access_key_value,associate_tag=associate_tag_value,locale='us')


# get all books from result set and
# print author and title
for seachResult in apiAmazon.item_search('All', Keywords='Disc%20Brake%20Pad%20and%20Caliper'):
    print seachResult.ItemAttributes.Title


apiAmazon = API(locale='us')
