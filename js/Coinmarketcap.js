class Coinmarketcap {
    constructor(scraper) {
        this.scraper = scraper;
        this.urls = {
            v1 : "https://api.coinmarketcap.com/v1/ticker/"
        }
    }

    scrape() {
        var promise = new Promise(function (resolve, reject) {
            this.scraper.https.get(this.urls.v1, function (res) {
                var fullData = '';
                res.on('data', function (chunk) {
                    fullData += chunk;
                });
                res.on('end', function () {
                    resolve(fullData);
                }.bind(this));

                res.on('error', function(err) {
                    sys.debug('unable to connect to ' + host);
                    reject(err);
                }.bind(this));

            }.bind(this));
        }.bind(this)).then(function (result) {
            try {
                var currencies = JSON.parse(result);
                var retval = [];

                for (var i = 0; i  < currencies.length; i++) {
                   
                    var cur = currencies[i];
                    cur.id = cur.id.replace(/-/g, "_");
                    if (this.scraper.currencies.includes(cur.id)) {
                        if(cur.max_supply === null) {
                            cur.max_supply = '0';
                        }
                        retval.push(this.scraper.setCurrencyValue(cur.id, cur.last_updated, cur.price_usd, cur.price_btc, cur["24h_volume_usd"], cur.market_cap_usd, cur.available_supply, cur.total_supply, cur.max_supply))
                    }
                }
                return retval;
            } catch(e) {
               return null;
            }
        }.bind(this));
        return promise;
    };
};

module.exports = Coinmarketcap;