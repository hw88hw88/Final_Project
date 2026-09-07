"use strict";
const express = require("express");
const bodyParser = require("body-parser");
const app = express();

const port = 40082;
const host = '127.0.0.1';

try
{
  app.use(bodyParser.urlencoded({ extended: true }));
  app.use(express.json());

  // Error handler middleware
  app.use((err, req, res, next) => {
    console.error(err.stack); // Log the stack trace to the console
    res.status(500).send('Something went wrong!'); // Send a custom error message to the client
  });

  require("./routes/main")(app);
  app.use(express.static("./public"));
  app.use("/img", express.static(__dirname + "public/img/"));
  app.use("/style", express.static(__dirname + "public/style/"));
  app.use("/script", express.static(__dirname + "public/script/"));

  app.set("views", "./views");
  app.set("view engine", "ejs");
  app.engine("html", require("ejs").renderFile);

  // Web server
  app.listen(port, host, () => console.log(`Running on port ${port}!`));
}
catch(ex)
{
  console.error("(index)Name: " + ex.name);
  console.error("Message: " + ex.message);
}