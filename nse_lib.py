import datetime
from pandas import read_csv, Series
import requests
import json
import math
from bs4 import BeautifulSoup
import csv



def conv_ctime(date=(2020, 1, 1)):
    return str(math.floor(datetime.datetime(date[0], date[1], date[2], 5, 30).timestamp()))

class Nse():  
    def __init__(self):
        pass

    def all_codes(self, give_json=False):
        equity_csv = 'https://archives.nseindia.com/content/equities/EQUITY_L.csv'
        df = read_csv(equity_csv)
        if give_json:
            return json.dumps(Series(df["NAME OF COMPANY"].values,index=df.SYMBOL).to_dict())
        return (Series(df["NAME OF COMPANY"].values,index=df.SYMBOL).to_dict())

    def get_intraday(self, code="", give_json=False):
        url = "https://in.finance.yahoo.com/quote/{}.NS".format(code.upper())
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html5lib")
        
        date = datetime.date.today()
        currprice = soup.select("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)")[0].text.replace(",", "")
        openprice = soup.select("#quote-summary > div.D\(ib\).W\(1\/2\).Bxz\(bb\).Pend\(12px\).Va\(t\).ie-7_D\(i\).smartphone_D\(b\).smartphone_W\(100\%\).smartphone_Pend\(0px\).smartphone_BdY.smartphone_Bdc\(\$seperatorColor\) > table > tbody > tr:nth-child(2) > td.Ta\(end\).Fw\(600\).Lh\(14px\) > span")[0].text.replace(",", "")
        prevprice = soup.select("#quote-summary > div.D\(ib\).W\(1\/2\).Bxz\(bb\).Pend\(12px\).Va\(t\).ie-7_D\(i\).smartphone_D\(b\).smartphone_W\(100\%\).smartphone_Pend\(0px\).smartphone_BdY.smartphone_Bdc\(\$seperatorColor\) > table > tbody > tr:nth-child(1) > td.Ta\(end\).Fw\(600\).Lh\(14px\) > span")[0].text.replace(",", "")
        volume = soup.select("#quote-summary > div.D\(ib\).W\(1\/2\).Bxz\(bb\).Pend\(12px\).Va\(t\).ie-7_D\(i\).smartphone_D\(b\).smartphone_W\(100\%\).smartphone_Pend\(0px\).smartphone_BdY.smartphone_Bdc\(\$seperatorColor\) > table > tbody > tr:nth-child(7) > td.Ta\(end\).Fw\(600\).Lh\(14px\) > span")[0].text.replace(",", "")
        
        ret = {"date": str(date.year)+"-"+str(date.month)+"-"+str(date.day), "price":currprice, "open":openprice, "volume":volume, "pclose":prevprice}
        
        if give_json:
            return json.dumps(ret)
        return ret
    
    def historical_data(self, code="", date_from=(2020, 1, 1), date_to=(2021, 1, 1), give_json=False):
        url = 'https://query1.finance.yahoo.com/v7/finance/download/{}.NS?period1={}&period2={}&interval=1d&events=history&includeAdjustedClose=true'.format(code.upper(), conv_ctime(date_from), conv_ctime(date_to))
        df = read_csv(url).to_dict("records")
        df.reverse()
        if give_json:
            return json.dumps(df)
        return (df)
    
    def live_quote(self, code=""):
        url = "https://in.finance.yahoo.com/quote/{}.NS".format(code.upper())
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html5lib")
        soup = soup.select("#quote-header-info > div.My\(6px\).Pos\(r\).smartphone_Mt\(6px\) > div.D\(ib\).Va\(m\).Maw\(65\%\).Ov\(h\) > div > span.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)")
        return (soup[0].text.replace(",", ""))

nse = Nse()

# print(nse.get_intraday("atgl"))


# print(nse.historical_data("reliance"))
print(nse.historical_data("reliance", give_json=True))
# print(nse.get_intraday("atgl"))

