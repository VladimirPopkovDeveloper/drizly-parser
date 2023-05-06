const puppeteer = require("puppeteer");
const fs = require("fs");

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--disabled-setuid-sandbox", "--no-sandbox"],
  });
  const page = await browser.newPage();
  await page.setExtraHTTPHeaders({
    "User-Agent":
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 Agency/97.8.6287.88",
  });

  const sitemapPath = "sitemapproducts.xml";
  const sitemapData = fs.readFileSync(sitemapPath, "utf8");
  const urls = sitemapData
    .match(/<loc>(.*?)<\/loc>/g)
    .map((s) => s.replace(/<\/?loc>/g, ""));
  console.log(`Loaded ${urls.length} URLs from ${sitemapPath}`);

  const badLinks = [];
  const scripts = [];

  const maxAttempts = 3;
  const maxIterations = 30;
  const delay = (milliseconds) =>
    new Promise((resolve) => setTimeout(resolve, milliseconds));

  for (let i = 0; i < urls.length && i < maxIterations; i++) {
    console.log(`Reading link №${i + 1}`);
    let attempts = 0;
    let success = false;
    while (!success && attempts < maxAttempts) {
      try {
        //const cacheUrl = `https://webcache.googleusercontent.com/search?q=cache:${urls[i]}`;
        await page.goto(urls[i], { waitUntil: "domcontentloaded" });
        success = true;
      } catch (error) {
        console.error(`Got unexpected error: ${error}`);
        attempts++;
        console.log(`Attempt #${attempts}`);
        await delay(Math.floor(Math.random() * (20000 - 5000 + 1) + 5000)); // Wait some random time
      }
    }

    if (!success) {
      console.log(`Failed to get response from server for link: ${urls[i]}`);
      badLinks.push(urls[i]);
      console.log(`Unprocessed link added to badlinks.txt`);
      fs.appendFileSync("badlinks.txt", `${urls[i]}\n`);
    } else {
      const scriptTag = await page.$(
        'script[data-hypernova-key="pdp_app_page"]'
      );
      const scriptContent = await page.evaluate(
        (scriptTag) => scriptTag.innerHTML,
        scriptTag
      );
      scripts.push(scriptContent);
      console.log(
        `Script content #${i + 1} for link ${urls[i]} added to scripts.json`
      );
      fs.appendFileSync("scripts.json", `${scriptContent}\n`);
    }
  }

  console.log(
    `Processed ${scripts.length} links, ${badLinks.length} links failed`
  );

  await browser.close();
})();
