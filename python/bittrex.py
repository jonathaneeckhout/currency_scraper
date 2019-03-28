#!/usr/bin/env python3
import requests
import mysql.connector
import json
import os

dirname = os.path.dirname(__file__)
configFile = os.path.join(dirname, '../mysql_config.json')

URL = "https://api.bittrex.com/api/v1.1/public/getmarketsummaries"

r = requests.get(url=URL)

data = r.json()

if data["success"] == True:
    with open(configFile) as json_data_file:
        config = json.load(json_data_file)

    mydb = mysql.connector.connect(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        passwd=config["password"],
        database=config["database"]
    )

    mycursor = mydb.cursor()

    for currency in data["result"]:
        currency["MarketName"] = currency["MarketName"].replace("-", "_")

        createTableSql = 'CREATE TABLE IF NOT EXISTS`currencies`.`' + currency['MarketName'] + \
            '`( `id` INT NOT NULL AUTO_INCREMENT ,  `TimeStamp` TIMESTAMP NOT NULL,  `High` FLOAT NOT NULL ,  `Low` FLOAT NOT NULL ,  `Volume` FLOAT NOT NULL ,  `Last` FLOAT NOT NULL ,  `BaseVolume` FLOAT NOT NULL ,  `Bid` FLOAT NOT NULL ,  `Ask` FLOAT NOT NULL ,  `OpenBuyOrders` INT NOT NULL ,  `OpenSellOrders` INT NOT NULL ,  `PrevDay` FLOAT NOT NULL ,    PRIMARY KEY  (`id`)) ENGINE = InnoDB;'
        mycursor.execute(createTableSql)
        mydb.commit()

        sql = 'INSERT INTO ' + currency['MarketName'] + ' (TimeStamp, High, Low, Volume, Last, BaseVolume, Bid, Ask, OpenBuyOrders, OpenSellOrders, PrevDay) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        val = (currency["TimeStamp"], currency["High"], currency["Low"], currency["Volume"],currency["Last"],currency["BaseVolume"],currency["Bid"],currency["Ask"],currency["OpenBuyOrders"], currency["OpenSellOrders"], currency["PrevDay"])
        mycursor.execute(sql, val)
        mydb.commit()

else:
    print("Bittrex request failed")
