#!/usr/bin/env python3
import requests
import mysql.connector
import json

currencies = [
    "bitcoin",
    "ethereum",
    "ripple",
    "litecoin",
    "eos",
    "bitcoin_cash",
    "binance_coin",
    "tether",
    "stellar",
    "cardano"
]

URL = "https://api.coinmarketcap.com/v1/ticker/"

r = requests.get(url=URL)

data = r.json()

transformedCurrencies = []

for currency in data:
    currency["id"] = currency["id"].replace("-", "_")
    if currency["id"] in currencies:
        # print(currency["symbol"])
        if currency["max_supply"] == None:
            currency["max_supply"] = 0
        transformedCurrencies.append({
            'id': currency["id"],
            'time': currency["last_updated"],
            'price': currency["price_usd"],
            'price_btc': currency["price_btc"],
            'volume_24h': currency["24h_volume_usd"],
            'market_cap': currency["market_cap_usd"],
            'available_supply': currency["available_supply"],
            'total_supply': currency["total_supply"],
            'max_supply': currency["max_supply"]
        })

#print(transformedCurrencies)

# Open config file
with open('../mysql_config.json') as json_data_file:
    config = json.load(json_data_file)

#print(config)

mydb = mysql.connector.connect(
    host=config["host"],
    port=config["port"],
    user=config["user"],
    passwd=config["password"],
    database=config["database"]
)

mycursor = mydb.cursor()

for curr in currencies:
    createTableSql = 'CREATE TABLE IF NOT EXISTS`currencies`.`' + curr + '`( `id` INT NOT NULL AUTO_INCREMENT , `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP , `price` FLOAT NOT NULL , `price_btc` FLOAT NOT NULL , `volume_24h` FLOAT NOT NULL , `market_cap` INT NOT NULL , `available_supply` INT NOT NULL , `total_supply` INT NOT NULL , `max_supply` INT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;'
    mycursor.execute(createTableSql)

mydb.commit()


#print(mydb) 