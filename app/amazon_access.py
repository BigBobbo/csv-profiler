from amazonproduct import API
from test1 import *


import amazonproduct


apiAmazon = API(access_key_id=access_key_id_value,secret_access_key=secret_access_key_value,associate_tag=associate_tag_value,locale='us')

def AmazonItems(sellerDF):
    Amazon_listDF = pd.DataFrame()
    for j in sellerDF.index:
        print "outer" + str(j)
        try:
            outerItemCall = apiAmazon.item_search('All', Keywords=sellerDF.Ebay_Title[j].replace('New!', ''), ResponseGroup='OfferFull', Condition='New',Availability='Available' )
            for i in range(0,(len(outerItemCall.page(1).Items.getchildren())-4)):
                print "inner" + str(i)
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



# from amazon.api import AmazonAPI
# apiAmazon = AmazonAPI(access_key_id_value, secret_access_key_value, associate_tag_value)


# def AmazonItems(sellerDF):
#     TitleList = []
#     PriceList = []
#     CurrencyList = []
#     ImageList = []
#     LinkList = []
#     for i in sellerDF.index:
#         time.sleep(2) # delays for 5 seconds
#         print i
#         try:
#             try:
#                 products = apiAmazon.search_n(1, Keywords=sellerDF.Ebay_Title[i], SearchIndex='All')
#             except:
#                 time.sleep(3) # delays for 5 seconds
#                 products = apiAmazon.search_n(1, Keywords=sellerDF.Ebay_Title[i], SearchIndex='All')
#                 print "wait"
#         except:
#             time.sleep(5) # delays for 5 seconds
#             products = apiAmazon.search_n(1, Keywords=sellerDF.Ebay_Title[i], SearchIndex='All')
#             print "wait2"
#         try:
#             TitleList.append(products[0].title)
#         except:
#             TitleList.append('Not Found')
#         try:
#             PriceList.append(products[0].price_and_currency[0])
#         except:
#             PriceList.append('Not Found')
#         try:
#             CurrencyList.append(products[0].price_and_currency[1])
#         except:
#             CurrencyList.append('Not Found')
#         try:
#             ImageList.append(products[0].small_image_url)
#         except:
#             ImageList.append('Not Found')
#         try:
#             LinkList.append(products[0].offer_url)
#         except:
#             LinkList.append('Not Found')
#         # except:
#         #     print "Fail"
#     amazonDF = pd.DataFrame({"Amazon_Title": TitleList, "Amazon_Price":PriceList, "Amazon_Currency":CurrencyList, "Amazon_ImageURL":ImageList, "Amazon_Link":LinkList })
#     return amazonDF
