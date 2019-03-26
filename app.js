var Scraper = require("./js/Scraper")

//var scraper = new Scraper(10 * 60 * 1000); // every 10 minutes
var scraper = new Scraper(10 * 1000); // every 10 minutes

scraper.init();

scraper.start();
