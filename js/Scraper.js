var Coinmarketcap = require('./Coinmarketcap');

class Scraper {
    constructor(interval) {
        this.https = require('https');
        this.fs = require('fs');
        this.interval = interval;
        this.sites = [];
        this.timer = undefined;
    };

    scrapeAll() {
        console.log("Scraping All sites");
        var promises = [];
        for (var site in this.sites) {
            promises.push(this.sites[site].scrape());
        }
        Promise.all(promises).then(function (data) {
            console.log("Scraped all sites. Merging and storing data");
            console.log(data);
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
        this.sites.push(new Coinmarketcap(this));
    };

};

module.exports = Scraper;