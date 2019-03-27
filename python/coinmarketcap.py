#!/usr/bin/env python3
import requests
import mysql.connector

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
            currency["max_supply"] =0
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

print(transformedCurrencies)
