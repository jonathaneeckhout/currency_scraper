var Coinmarketcap = require('./Coinmarketcap');

class Scraper {
    constructor(interval) {
        this.https = require('https');
        this.fs = require('fs');
        this.mysql = require('mysql');
        this.connection = null;
        this.connectionConfig = null;
        this.interval = interval;
        this.sites = [];
        this.currencies = [
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
        ];
        this.timer = undefined;
    };

    scrapeAll() {
        console.log("Scraping All sites");
        var promises = [];
        for (var site in this.sites) {
            promises.push(this.sites[site].scrape());
        }
        Promise.all(promises).then(function (data) {
            this.connection = this.mysql.createConnection(this.connectionConfig);
            for (var i = 0; i < data.length; i++) {
                this.pushDataToMysql(data[i]);
            }
            this.connection.end();
        }.bind(this));
    };

    start() {
        this.scrapeAll();
        this.timer = setInterval(this.scrapeAll.bind(this), this.interval);
    };

    stop() {
        clearInterval(this.timer);
    };

    init() {
        var rawMysqlConfig = this.fs.readFileSync('mysql_config.json');
        this.connectionConfig = JSON.parse(rawMysqlConfig);

        this.sites.push(new Coinmarketcap(this));
    };

    pushDataToMysql(data) {
        for (var i = 0; i < data.length; i++) {
            var cur = data[i];
            let sql = 'INSERT INTO ' + cur.id + '(price, price_btc,volume_24h,market_cap,available_supply,total_supply,max_supply) VALUES(' 
            + cur.price +','
            + cur.price_btc +','
            + cur.volume_24h +','
            + cur.market_cap +','
            + cur.available_supply +','
            + cur.total_supply +','
            + cur.max_supply +
            ')';

            // execute the insert statment
            this.connection.query(sql, function (error, results, fields) {
                if (error) console.log(error);
            });
        }
    }

    setCurrencyValue(id, time, price, price_btc, volume_24h, market_cap, available_supply, total_supply, max_supply) {
        return {
            id: id,
            time: time,
            price: price,
            price_btc: price_btc,
            volume_24h: volume_24h,
            market_cap: market_cap,
            available_supply: available_supply,
            total_supply: total_supply,
            max_supply: max_supply
        }
    }

};

module.exports = Scraper;