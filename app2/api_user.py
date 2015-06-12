from ebaysdk.trading import Connection as Trading
from ebaysdk.shopping import Connection as Shopping
from test1 import *

# import math
import pandas as pd
# import time

# for testing
# import datetime
# from xml.etree.ElementTree import ElementTree

######################################################################
# Ebay
######################################################################

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

######################################################################
# Amazon
######################################################################

from amazonproduct import API
import amazonproduct

apiAmazon = API(access_key_id=access_key_id_value,secret_access_key=secret_access_key_value,associate_tag=associate_tag_value,locale='us')


def AmazonItems(sellerDF):
    Amazon_listDF = pd.DataFrame()
    for j in sellerDF.index:
        # print "outer" + str(j)
        try:
            outerItemCall = apiAmazon.item_search('All', Keywords=sellerDF.Ebay_Title[j].replace('New!', ''), ResponseGroup='OfferFull', Condition='New',Availability='Available' )
            for i in range(0,(len(outerItemCall.page(1).Items.getchildren())-4)):
                # print "inner" + str(i)
                if outerItemCall.page(1).Items.Item[i].Offers.Offer.OfferListing.IsEligibleForSuperSaverShipping == 1:
                    Amazon_numAvailible = str(outerItemCall.page(1).Items.Item[i].OfferSummary.TotalNew)
                    Amazon_currency = str(outerItemCall.page(1).Items.Item[i].Offers.Offer.OfferListing.Price.CurrencyCode)
                    Amazon_value = (outerItemCall.page(1).Items.Item[i].Offers.Offer.OfferListing.Price.getchildren()[0]/100.0)
                    Amazon_price = str(outerItemCall.page(1).Items.Item[i].Offers.Offer.OfferListing.Price.FormattedPrice)
                    # link = outerItemCall.page(1).Items.Item[i].Offers.MoreOffersUrl #DetailPageURL neither links are great
                    Amazon_link = str(outerItemCall.page(1).Items.Item[i].Offers.getchildren()[2] )
                    innerImageCall = apiAmazon.call(Operation='ItemLookup', ItemId=outerItemCall.page(1).Items.Item[i].getchildren()[0], ResponseGroup='Medium')
                    Amazon_title = str(innerImageCall.Items.Item.ItemAttributes.Title)
                    Amazon_thumbnail = str(innerImageCall.Items.Item.SmallImage.getchildren()[0])
                    break
                else:
                    Amazon_numAvailible = "None Availible"
                    Amazon_currency = "NA"
                    Amazon_price = "NA"
                    Amazon_link = "NA"
                    Amazon_title = "None Shippable Availible"
                    Amazon_thumbnail = "None Availible"
                    Amazon_value = sellerDF.Ebay_Price[j]
        except:
            Amazon_numAvailible = "None Availible"
            Amazon_currency = "NA"
            Amazon_price = "NA"
            Amazon_link = "NA"
            Amazon_title = "None Availible"
            Amazon_thumbnail = "None Availible"
        Amazon_lineDF = pd.DataFrame({"Amazon_Title": Amazon_title, "Amazon_Quant_Availible":Amazon_numAvailible, "Amazon_Price":Amazon_price, "Amazon_Currency":Amazon_currency, "Amazon_ImageURL":Amazon_thumbnail, "Amazon_Link":Amazon_link, "Amazon_Value":Amazon_value },index=[0])
        Amazon_listDF = Amazon_listDF.append(Amazon_lineDF)
        Amazon_listDF = Amazon_listDF.reset_index(drop=True)
    return Amazon_listDF

######################################################################
# Combine
######################################################################

def comparisonTable(EbayUser,tableSize):
    EbayDF = ListSellersItems(EbayUser,tableSize)
    AmazonDF = AmazonItems(EbayDF)
    result = pd.concat([EbayDF, AmazonDF], axis=1, join_axes=[EbayDF.index])
    result.priceDiff = result.Ebay_Price.astype(float) - result.Amazon_Value.astype(float)
    result['Arb_Chance'] = result.Ebay_Price.astype(float) - result.Amazon_Value.astype(float)
    result.sort('Arb_Chance', ascending=False, inplace=False)
    return result.sort(['Arb_Chance'], ascending=False).reset_index(drop=True)

def comparisonTableHtml(EbayUser,tableSize):
    outputlist = []
    EbayDF = ListSellersItems(EbayUser,tableSize)
    AmazonDF = AmazonItems(EbayDF)
    result = pd.concat([EbayDF, AmazonDF], axis=1, join_axes=[EbayDF.index])
    result.priceDiff = result.Ebay_Price.astype(float) - result.Amazon_Value.astype(float)
    result['Arb_Chance'] = result.Ebay_Price.astype(float) - result.Amazon_Value.astype(float)
    result.sort('Arb_Chance', ascending=False, inplace=False)
    result = result.sort(['Arb_Chance'], ascending=False).reset_index(drop=True)
    for i in result.index:
        tableRow =  "<td>" + str(result.Ebay_Currency[i])  + "</td><td>" + \
        str(result.Ebay_End[i])  + \
        "</td><td><a href=" + result.Ebay_Link[i] + "><img src='" + str(result.Ebay_ImageURL[i]) + "' alt='' border=3 height=100 width=100></img></td><td></a>" + \
        str(result.Ebay_Price[i])  + "</td><td>" + \
        str(result.Ebay_Title[i])  + "</td><td>" + \
        str(result.Amazon_Currency[i])  + \
        "</td><td><a href=" + result.Amazon_Link[i] + "><img src='" + str(result.Amazon_ImageURL[i]) + "' alt='' border=3 height=100 width=100></img></td><td></a>" + \
        str(result.Amazon_Price[i])  + "</td><td>" + \
        str(result.Amazon_Quant_Availible[i])  + "</td><td>" + \
        str(result.Amazon_Title[i])  + "</td><td>" + \
        str(result.Amazon_Value[i])  + "</td><td>" + \
        str(result.Arb_Chance[i]) + "</td>"
        outputlist.append(tableRow)
    return  outputlist



######################################################################
# Test
######################################################################

# starttime = datetime.datetime.time(datetime.datetime.now())
# comparisonTableHtml('nikkzakk',2)
# endtime = datetime.datetime.time(datetime.datetime.now())
# end
