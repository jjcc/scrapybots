
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymarketcap import Pymarketcap

def main():
    cmc = Pymarketcap()

    # Get all currencies ranked by volume
    currencies = cmc.ticker()
    num = currencies['metadata']['num_cryptocurrencies']
    data = currencies['data']

    file = "marketcap.csv"
    with open(file, 'w') as outfile:
        line = "id,name,symbol,website_slug,rank,circulating,total,max,market,last_update\n"
        outfile.write(line)
        for id, info in data.items():
            print("###%s"%info['symbol'])
            line = ""
            for key,value in info.items():
                if key != "quotes":
                    #print("%s:%s"%(key, value))
                    line = line + str(value) +  ","
                else:
                    #print("market:%s"%value["USD"]["market_cap"])
                    line = line + str(value["USD"]["market_cap"]) + ","
            outfile.write(line + "\n")

    #for c in currencies:


    print(currencies)

if __name__ == "__main__":
    main()
