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
                return JSON.parse(result);
            } catch(e) {
               return null;
            }
        }.bind(this));
        return promise;
    };
};

module.exports = Coinmarketcap;