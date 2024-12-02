const http = require('http');
const fs = require('fs');
const path = require('path');

const hostname = '127.0.0.1';
const port = 7000;

const server = http.createServer((req, res) => {
  let retData = "";
  if (req.url === '/') {
    fs.readFile(path.join(__dirname, 'article.json'), 'utf8', (err, data) => {
      if (err) {
        res.statusCode = 500;
        res.end(JSON.stringify({ error: 'Could not read data' }));
        return;
      }
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json');
      const jsonData = JSON.parse(data)
      const data_2 = jsonData[2]

      for (i in jsonData[2]["data"]) {
        let cData = data_2.data[i]
        retData += (
          "Id Article: " + cData.id_article
          + "\n Nom Ar" + cData.nom
          + " \nRédigé par: " + cData.auteur
          + " \Date de publication: " + cData.date_de_publication
          + "\nContenu" + cData.contenu
          + "\n ====================  END OF OBJECT ===============> \n\n");
      }

      //console.log(retData);
      res.end(retData);

    });
  } else {
    res.statusCode = 404;
    res.end(JSON.stringify({ error: 'Not found' }));
  }
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
