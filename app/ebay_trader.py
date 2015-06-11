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




def ListSellersItems(UserID,entries):
    responseSeller = apiTrade.execute('GetSellerList', {'UserID':UserID,'EndTimeFrom':'2015-06-11T19:09:02','EndTimeTo':'2015-07-09T00:09:02',  'GranularityLevel':'Medium', 'Pagination':{'EntriesPerPage':entries, 'PageNumber':1}})
    TitleList = [item.Title for item in responseSeller.reply.ItemArray.Item]
    PriceList = [item.SellingStatus.ConvertedCurrentPrice.value for item in responseSeller.reply.ItemArray.Item]
    CurrencyList = [item.SellingStatus.ConvertedCurrentPrice._currencyID for item in responseSeller.reply.ItemArray.Item]
    ImageList = [item.PictureDetails.PictureURL[0] for item in responseSeller.reply.ItemArray.Item]
    LinkList = [item.ListingDetails.ViewItemURL for item in responseSeller.reply.ItemArray.Item]
    EndDateList = [item.ListingDetails.EndTime for item in responseSeller.reply.ItemArray.Item]
    sellerDFPage = pd.DataFrame({"Ebay_Title": TitleList, "Ebay_Price":PriceList, "Ebay_Currency":CurrencyList, "Ebay_End":EndDateList, "Ebay_ImageURL":ImageList, "Ebay_Link":LinkList })
    # Check Datatype of dates and see if table can be arranged by price and date
    # sellerDFPage.sort_index(by=['Ebay_Price', 'Ebay_Link'], ascending=[False, False])
    # Ensure that this is acting in place
    return sellerDFPage


# ListSellersItems('nikkzakk')
# UserID = 'nikkzakk'


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
