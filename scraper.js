// Using ScrapingAntClient Libs
const ScrapingAntClient = require("@scrapingant/scrapingant-client");
const cheerio = require("cheerio");
const fs = require("fs").promises;
const { parseStringPromise } = require("xml2js");

const client = new ScrapingAntClient({
  apiKey: "e95b043e4a614c79ac7a0ef47757d8c9",
});

async function main() {
  try {
    // Read XML data
    const data = await fs.readFile("sitemapproducts.xml");
    const result = await parseStringPromise(data);
    const links = result.urlset.url.map((url) => url.loc[0]);
    console.log("Links have recieved");

    // Get parse data
    for (const element of links) {
      const res = await client.scrape(element);
      const $ = cheerio.load(res.content);
      $(
        'script[type="application/json"][data-hypernova-key="pdp_app_page"]'
      ).each(function () {
        const scriptContent = $(this)
          .html() // Get content of script tag
          .replace(/<!--|-->/g, ""); // Remove comment markup
        console.log(scriptContent);
      });
    }
  } catch (err) {
    console.error(err.message);
  }
}

main();
