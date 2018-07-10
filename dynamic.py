import pandas as pd
import numpy as np
import json
from pandas import DataFrame
import re
from datetime import datetime
import py_yahoo_prices.price_fetcher as pf

# start date
st_dt = datetime(2008, 1, 1)

world_indexes = {
    '^GSPC':'S&P 500',
    '^DJI':'Dow 30',
    '^IXIC':'Nasdaq',
    '^NYA':'NYSE COMPOSITE (DJ)',
    '^XAX':'NYSE AMEX COMPOSITE INDEX',
    '^BATSK':'BATS 1000 Index',
    '^RUT':'Russell 2000',
    '^VIX':'Vix',
    '^FTSE':'FTSE 100',
    '^GDAXI':'DAX PERFORMANCE-INDEX',
    '^FCHI':'CAC 40',
    '^STOXX50E':'ESTX 50 PR.EUR',
    '^N100':'EURONEXT 100',
    '^BFX':'BEL 20',
    'MICEXINDEXCF.ME':'MICEX Index',
    '^N225':'Nikkei 225',
    '^HSI':'HANG SENG INDEX',
    '000001.SS':'SSE Composite Index',
    '^STI':'STI Index',
    '^AXJO':'S&P/ASX 200',
    '^AORD':'ALL ORDINARIES',
    '^BSESN':'S&P BSE SENSEX',
    '^JKSE':'Jakarta Composite Index',
    '^KLSE':'FTSE Bursa Malaysia KLCI',
    '^NZ50':'S&P/NZX 50 INDEX GROSS',
    '^KS11':'KOSPI Composite Index',
    '^TWII':'TSEC weighted index',
    '^GSPTSE':'S&P/TSX Composite index',
    '^BVSP':'IBOVESPA',
    '^MXX':'IPC MEXICO',
    '^IPSA':'IPSA SANTIAGO DE CHILE',
    '^MERV':'MERVAL',
    '^TA100':'TA-125',
    '^CASE30':'EGX 30 Price Return Index',
    'JN0U.FGI':'FTSE/JSE TOP 40 USD'
}

filename = "AUTO"


# Generate correlation matrix and d3 json, save to file
def genfile(comp_codes):
    # get the raw prices from yahoo, auto retries on a 401 error
    raw_prices = pf.multi_price_fetch(comp_codes, start_date=st_dt, interval='1d')

    datafram = pd.DataFrame(columns=comp_codes)

    i = 0
    for code in comp_codes:
        try:
            df = raw_prices[code]
            df1 = df.assign(Daily_Change=pd.Series(np.random.randn(len(df['Date']))).values)
            df1.at[0, 'Daily_Change'] = 0
            for index, row in df1.iterrows():
                # calculate daily percentage change
                try:
                    df1.at[index+1, 'Daily_Change'] = ((df1.at[index+1, 'Adj Close']-df1.at[index, 'Adj Close'])/df1.at[index, 'Adj Close'])
                except Exception:
                    pass
            datafram[code] = df1['Daily_Change']
            print(str(i) + ": " + code)
            i+=1
        except Exception:
            print("Error with code " + code)

    t = datafram.corr()
    l = []

    names = [""]+["Group"]+t.columns.values.tolist()

    i = 0
    for index, row in t.iterrows():
        r = [names[i+2]]+[i%50]+row.tolist()
        l.append(r)
        i += 1

    d2 = pd.DataFrame(l, columns=names)

    #print(d2)

    fnmcsv = filename+".csv"
    d2.to_csv(fnmcsv, index=False)

    # GENERATE D3 CHART SECTION
    r = open(fnmcsv, "r")
    file = r.read()

    data = []
    temp = file.split("\n")

    for row in temp:
        if row != '':
            s = re.split('(?!\B"[^"]*),(?![^"]*"\B)', row)
            data.append(s)

    df = DataFrame(data=data)

    print(df)

    # CREATE NODE
    node = []
    for i in range(1, df.shape[0]):
        node.append({"name": df[0][i], "group": float(df[1][i])})
        print(i)

    print(node)

    # CREATE LINK
    link = []
    for i in range(3, df.shape[1] + 1):
        for j in range(2, i - 1):
            link.append({"source": i - 3, "target": j - 2, "value": df[i - 1][j - 1]})

    # DEFAULT OPTION
    option = [{
        "chart_type": "structure_graph",
        "color": "",
        "cutoff": "",
        "radious": "",
        "link_strength": "",
        "schema_size": "",
        "edge_bundle": "",
    }
    ]

    # to json
    chart_data = json.dumps({"nodes": node, "links": link})
    chart_option = json.dumps({"option": option})
    result = {"chart_data": chart_data, "chart_option": chart_option}

    print(chart_data)

    fnmjson = filename+".json"
    f = open(fnmjson, "w")
    f.write(chart_data)