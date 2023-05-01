const puppeteer = require("puppeteer");
const cheerio = require("cheerio");

const getBooksData = async () => {
  const url =
    "https://drizly.com/wine/white-wine/sauvignon-blanc/cloudy-bay-sauvignon-blanc/p2734";
  browser = await puppeteer.launch({
    headless: true,
    args: ["--disabled-setuid-sandbox", "--no-sandbox"],
  });
  const page = await browser.newPage();
  await page.setExtraHTTPHeaders({
    "User-Agent":
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 Agency/97.8.6287.88",
  });
  await page.goto(url, { waitUntil: "domcontentloaded" });

  // Finding the element containing JSON data using Cheerio
  const hypernovaData = await page.evaluate(() => {
    const $ = window.$ || window.jQuery;
    const scriptData = $(
      'script[type="application/json"][data-hypernova-key="pdp_app_page"]'
    ).html();
    console.log(scriptData);
  });

  await browser.close();
};

getBooksData();
