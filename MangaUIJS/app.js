let mongoose = require("mongoose");
let manga = require("./mangaSchema.js");
let ini = require("node-ini");

let config = ini.parseSync("../Database-Script/db_config.ini", "utf-8");

let test = config[Object.keys(config)];
let connection_uri = test[Object.keys(test)[0]];

mongoose.connect(connection_uri, {
  useUnifiedTopology: true,
  useNewUrlParser: true,
});

const connection = mongoose.connection;

connection.once("open", async function () {
  console.log("MongoDB database connection established successfully");
  try {
    var mangaData = await manga.find({});
  } catch (err) {
    console.log(err);
  } finally {
    connection.close();
    console.log("Connection has been closed");
    doSmtgData(mangaData);
  }
});

function doSmtgData(mangaData) {
  console.log(mangaData);
}
