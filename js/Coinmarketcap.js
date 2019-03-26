class Coinmarketcap {
    constructor() {
        this.urls = {
            v1 : "https://api.coinmarketcap.com/v1/ticker/"
        }
    }

    scrape() {
        console.log("Getting currency data");

        var promise = new Promise(function (resolve, reject) {
            resolve(true);
        });

    }
};

module.exports = Coinmarketcap;