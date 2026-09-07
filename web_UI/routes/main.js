module.exports = (app) => 
{
  try 
  {
    // render pages
    const pageRender = (req, res, next, htmlFilePath) => {
      try
      {
        // render page
        return res.render(htmlFilePath);
      } catch (ex) {
        console.log("Name (pageRender): " + ex.name);
        console.log("Message: " + ex.message);
        return res.render("error.html");
      }
    }

    app.get("/about", (req, res, next) => {
      pageRender(req, res, next, "about.html");
    });

    /**************************************************** */
    // render page with variables
    const pageRenderVar = (req, res, next, htmlFilePath, htmlContent) => {
      try
      {
        return res.render(htmlFilePath, htmlContent);
      } catch (ex) {
        console.log("Name (pageRenderVar): " + ex.name);
        console.log("Message: " + ex.message);
        return res.render("error.html");
      }
    }

    app.get("/", (req, res, next) => {
      pageRenderVar(req, res, next, "index.html", {
        feedback: "",
        name: "",
        email: "",
        message: "",
        sender: "",
      });
    });
    /**************************************************** */

    app.post("/", (req, res, next) => {
      const send_to_flask = require('./api_flask.js');
      const chatbot_response = async () => {
        const response = await send_to_flask.send_to_chatbot(req.body);
        return res.send({
          "text": response.text,
          "sender": response.sender,
        });
      };
      chatbot_response();
    });
  } 
  catch (ex) 
  {
    console.log("(Main)Name: " + ex.name);
    console.log("Message: " + ex.message);
  }
};
