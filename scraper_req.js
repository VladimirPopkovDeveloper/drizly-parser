const cheerio = require("cheerio");
const fs = require("fs").promises;
const { parseStringPromise } = require("xml2js");
const axios = require("axios");

async function main() {
  try {
    // Read XML data
    const data = await fs.readFile("sitemapproducts.xml");
    const result = await parseStringPromise(data);
    const links = result.urlset.url.map((url) => url.loc[0]);
    console.log("Links have received");

    // Get parse data
    for (const element of links) {
      let attempts = 0;
      const maxAttempts = 3;
      while (attempts < maxAttempts) {
        try {
          const response = await axios.get(element);
          const $ = cheerio.load(response.data);
          $(
            'script[type="application/json"][data-hypernova-key="pdp_app_page"]'
          ).each(function () {
            const scriptContent = $(this)
              .html() // Get content of script tag
              .replace(/<!--|-->/g, ""); // Remove comment markup
            console.log(scriptContent);
          });
          break;
        } catch (error) {
          console.error(`Attempt ${attempts + 1} failed for ${element}`);
          if (attempts === maxAttempts - 1) {
            console.error(`Could not retrieve content for ${element}`);
          }
        }
        attempts++;
      }
    }
  } catch (err) {
    console.error(err.message);
  }
}

main();
