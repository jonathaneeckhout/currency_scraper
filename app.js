var Scraper = require("./js/Scraper")

var scraper = new Scraper(60 * 1000);

scraper.init();

scraper.start();
