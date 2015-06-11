from ebaysdk.trading import Connection as Trading
from ebaysdk.shopping import Connection as Shopping

from test1 import *

import math
import pandas as pd
import time

# for testing
import datetime
from xml.etree.ElementTree import ElementTree

apiTrade = Trading(appid=appid, devid=devid, certid=certid, token=token,config_file=None)
apiShop = Shopping(appid=appid,config_file=None)


# def ListSellersItems(UserID):
#     responseSeller = apiTrade.execute('GetSellerList', {'UserID':UserID,'EndTimeFrom':'2015-06-05T19:09:02','EndTimeTo':'2015-07-09T00:09:02',  'GranularityLevel':'Fine', 'Pagination.EntriesPerPage':25, 'Pagination.PageNumber':1})
#     ItemList = [item.ItemID for item in responseSeller.reply.ItemArray.Item]
#     sellerDF = pd.DataFrame()
#     # for i in range(0,1):
#     for i in range(0,min(int(math.ceil(len(ItemList)/20.0)),10)):
#         print i
#         responseShop = apiShop.execute('GetMultipleItems', {'itemID':ItemList[(0+(i*20)):(20+(i*20))]})
#         # responseShop.reply.Item.___ for different attribute
#         TitleList = [item.Title for item in responseShop.reply.Item]
#         PriceList = [item.ConvertedCurrentPrice.value for item in responseShop.reply.Item]
#         CurrencyList = [item.ConvertedCurrentPrice._currencyID for item in responseShop.reply.Item]
#         ImageList = [item.GalleryURL for item in responseShop.reply.Item]
#         LinkList = [item.ViewItemURLForNaturalSearch for item in responseShop.reply.Item]
#         sellerDFPage = pd.DataFrame({"Ebay_Title": TitleList, "Ebay_Price":PriceList, "Ebay_Currency":CurrencyList, "Ebay_ImageURL":ImageList, "Ebay_Link":LinkList })
#         sellerDF = sellerDF.append(sellerDFPage)
#     # May change this to append multiple calls of <20 together
#     return sellerDF


def ListSellersItems(UserID):
    responseSeller = apiTrade.execute('GetSellerList', {'UserID':UserID,'EndTimeFrom':'2015-06-11T19:09:02','EndTimeTo':'2015-07-09T00:09:02',  'GranularityLevel':'Medium', 'Pagination':{'EntriesPerPage':1, 'PageNumber':1}})
    ItemList = [item.ItemID for item in responseSeller.reply.ItemArray.Item]
    PriceList = [item.SellingStatus.ConvertedCurrentPrice for item in responseSeller.reply.ItemArray.Item]
    # Change this so it all comes from the first call
    sellerDF = pd.DataFrame()
    # for i in range(0,1):
    for i in range(0,min(int(math.ceil(len(ItemList)/20.0)),10)):
        print i
        responseShop = apiShop.execute('GetMultipleItems', {'itemID':ItemList[(0+(i*20)):(20+(i*20))]})
        # responseShop.reply.Item.___ for different attribute
        TitleList = [item.Title for item in responseShop.reply.Item]
        PriceList = [item.ConvertedCurrentPrice.value for item in responseShop.reply.Item]
        CurrencyList = [item.ConvertedCurrentPrice._currencyID for item in responseShop.reply.Item]
        ImageList = [item.GalleryURL for item in responseShop.reply.Item]
        LinkList = [item.ViewItemURLForNaturalSearch for item in responseShop.reply.Item]
        sellerDFPage = pd.DataFrame({"Ebay_Title": TitleList, "Ebay_Price":PriceList, "Ebay_Currency":CurrencyList, "Ebay_ImageURL":ImageList, "Ebay_Link":LinkList })
        sellerDF = sellerDF.append(sellerDFPage)
    # May change this to append multiple calls of <20 together
    return sellerDF


# ListSellersItems('nikkzakk')
# UserID = 'nikkzakk'
responseSeller = apiTrade.execute('GetSellerList', {'UserID':UserID,'EndTimeFrom':'2015-06-11T19:09:02','EndTimeTo':'2015-07-09T00:09:02',  'GranularityLevel':'Coa', 'Pagination':{'EntriesPerPage':1, 'PageNumber':1}})
[item.SellingStatus.ConvertedCurrentPrice for item in responseSeller.reply.ItemArray.Item]
.reply.ItemArray.Item.SellingStatus.ConvertedCurrentPrice

from amazon.api import AmazonAPI
apiAmazon = AmazonAPI(access_key_id_value, secret_access_key_value, associate_tag_value)


def AmazonItems(sellerDF):
    TitleList = []
    PriceList = []
    CurrencyList = []
    ImageList = []
    LinkList = []
    for i in sellerDF.index:
        time.sleep(2) # delays for 5 seconds
        print i
        try:
            try:
                products = apiAmazon.search_n(1, Keywords=sellerDF.Title[i], SearchIndex='All')
            except:
                time.sleep(3) # delays for 5 seconds
                products = apiAmazon.search_n(1, Keywords=sellerDF.Title[i], SearchIndex='All')
                print "wait"
        except:
            time.sleep(5) # delays for 5 seconds
            products = apiAmazon.search_n(1, Keywords=sellerDF.Title[i], SearchIndex='All')
            print "wait2"
        try:
            TitleList.append(products[0].title)
        except:
            TitleList.append('Not Found')
        try:
            PriceList.append(products[0].price_and_currency[0])
        except:
            PriceList.append('Not Found')
        try:
            CurrencyList.append(products[0].price_and_currency[1])
        except:
            CurrencyList.append('Not Found')
        try:
            ImageList.append(products[0].small_image_url)
        except:
            ImageList.append('Not Found')
        try:
            LinkList.append(products[0].offer_url)
        except:
            LinkList.append('Not Found')
        # except:
        #     print "Fail"
    amazonDF = pd.DataFrame({"Amazon_Title": TitleList, "Amazon_Price":PriceList, "Amazon_Currency":CurrencyList, "Amazon_ImageURL":ImageList, "Amazon_Link":LinkList })
    return amazonDF

starttime = datetime.datetime.time(datetime.datetime.now())
testdf = ListSellersItems('nikkzakk')
testdfamazon = AmazonItems(testdf)
result = pd.concat([testdf, testdfamazon], axis=1, join_axes=[testdf.index])
endtime = datetime.datetime.time(datetime.datetime.now())
