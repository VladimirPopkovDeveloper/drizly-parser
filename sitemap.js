const fs = require("fs");
const { parseString } = require("xml2js");

// Чтение содержимого файла и преобразование XML в объект JavaScript
fs.readFile("sitemapproducts.xml", (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  parseString(data, (err, result) => {
    if (err) {
      console.error(err);
      return;
    }
    // Извлечение списка ссылок из объекта JavaScript
    const links = result.urlset.url.map((url) => url.loc[0]);
    console.log(links);
  });
});
