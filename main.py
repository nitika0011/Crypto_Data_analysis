import pandas as pd
import datetime
import os
from time import time
from time import sleep
import matplotlib.pyplot as plt
import seaborn as sns
API="7d034d92-8c30-4b60-b058-dbeeeb659294"

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'15',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API  ,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        # print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    
    df =pd.json_normalize(data["data"])
    pd.set_option("display.max.columns",None)
    df["timestamp"]=pd.to_datetime("now")
    # df=pd.concat([df2,df2])
    print(df)
    
    if not os.path.isfile(r"C:\nitid\DATA_Analysis_Alex\Python\API.csv"):
        df.to_csv(r"C:\nitid\DATA_Analysis_Alex\Python\API.csv", header="column_names")
    else:
        df.to_csv(r"C:\nitid\DATA_Analysis_Alex\Python\API.csv", mode="a", header=False)
df = pd.read_csv(r"C:\nitid\DATA_Analysis_Alex\Python\API.csv")
# print(df)
# df=pd.set_option("display.float_format",lambda x:"%.5f" %x)
# pd.set_option("display.max.columns",50)
# print(df)
df3=df.groupby("name",sort=False)[["quote.USD.percent_change_1h","quote.USD.percent_change_24h","quote.USD.percent_change_7d",
                               "quote.USD.percent_change_30d","quote.USD.percent_change_60d",
                               "quote.USD.percent_change_90d"]].mean()

# print(df3)
df4 =df3.stack()
# print(df4)
df5=df4.to_frame(name="values")
# count_row=df5.count()
# print(count_row)

index=pd.Index(range(90))
df6= df5.reset_index()
# print(df6)
df7=df6.rename(columns={"level_1":"percent_change"})
print(df7)


sns.catplot(x="percent_change",y="values",hue="name",data=df7,kind="point",height=6,aspect=2)
# print(type(df5))


# for i in range(333):
#     api_runner()
#     print("API runner completed successfully!")
#     sleep(60)
# exit()


plt.show()