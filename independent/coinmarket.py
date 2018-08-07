#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd


from pymarketcap import Pymarketcap

def main():
    cmc = Pymarketcap()

    # Get all currencies ranked by volume
    currencies = cmc.ticker()
    num = currencies['metadata']['num_cryptocurrencies']
    data = currencies['data']

    file = "marketcap.csv"
    datain = []
    with open(file, 'w') as outfile:
        line = "id,name,symbol,website_slug,rank,circulating,total,max,market,last_update\n"
        outfile.write(line)
        for id, info in data.items():
            # for pd
            row = {}
            print("###%s"%info['symbol'])
            line = ""
            for key,value in info.items():
                if key != "quotes":
                    #print("%s:%s"%(key, value))
                    line = line + str(value) +  ","
                    row[key] = value
                else:
                    #print("market:%s"%value["USD"]["market_cap"])
                    line = line + str(value["USD"]["market_cap"]) + ","
                    row['market_cap'] = value["USD"]["market_cap"]
            outfile.write(line + "\n")
            datain.append(row)

    df = pd.DataFrame(datain)
    df["per"] = df['market_cap'] * 100 / df['market_cap'].sum()
    #subtotal
    subtotal = 0
    for k, v in df.iterrows():
        subtotal += v['per']
        print('per:' + str(v['per']) + ",assumulate:" + str(subtotal))


    print(df.head())
    print(df.tail())
    #for c in currencies:


    print(currencies)

if __name__ == "__main__":
    main()
