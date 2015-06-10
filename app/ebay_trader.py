from ebaysdk.trading import Connection as Trading
from ebaysdk.shopping import Connection as Shopping

from test1 import *

import math
import pandas as pd

apiTrade = Trading(appid=appid, devid=devid, certid=certid, token=token,config_file=None)
apiShop = Shopping(appid=appid,config_file=None)


def ListSellersItems(UserID):
    responseSeller = apiTrade.execute('GetSellerList', {'UserID':UserID,'EndTimeFrom':'2015-06-05T19:09:02','EndTimeTo':'2015-07-09T00:09:02'})
    ItemList = [item.ItemID for item in responseSeller.reply.ItemArray.Item]
    sellerDF = pd.DataFrame()
    for i in range(0,1):
    # for i in range(0,int(math.ceil(len(ItemList)/20.0))):
        responseShop = apiShop.execute('GetMultipleItems', {'itemID':ItemList[(0+(i*20)):(20+(i*20))]})
        # responseShop.reply.Item.___ for different attribute
        TitleList = [item.Title for item in responseShop.reply.Item]
        PriceList = [item.ConvertedCurrentPrice.value for item in responseShop.reply.Item]
        CurrencyList = [item.ConvertedCurrentPrice._currencyID for item in responseShop.reply.Item]
        ImageList = [item.GalleryURL for item in responseShop.reply.Item]
        LinkList = [item.ViewItemURLForNaturalSearch for item in responseShop.reply.Item]
        sellerDFPage = pd.DataFrame({"Ebay_Title": TitleList, "Ebay_Price":PriceList, "Ebay_Currency":CurrencyList, "Ebay_ImageURL":ImageList, "Ebay_Link":LinkList })
    return sellerDFPage

ListSellersItems('nikkzakk')


from amazon.api import AmazonAPI
apiAmazon = AmazonAPI(access_key_id_value, secret_access_key_value, associate_tag_value)
product = apiAmazon.lookup(ItemId='0316067938')


for i in range(0,int(math.ceil(len(testlist)/20.0))):
    print i


responseShop = apiShop.execute('GetMultipleItems', {'itemID':ItemList[(0):(20)]})