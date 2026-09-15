'use strict';

const chatbot_url = 'http://localhost:5005/webhooks/rest/webhook';

const sender_id = 'node_server';

const send_to_chatbot = async (message_input) => {
    const response = await fetch(chatbot_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
        },
        body: 
            JSON.stringify(
                {
                    'sender': sender_id,
                    'message': message_input
                }
            ),             
    });

    if (!response.ok)
    {
        throw new Error(`Server status: ` + response.status);
    }

    const json = await response.json();
    const result = json[0].text;
    return result;

};



// Export the functions so they can be imported by other JavaScript files.
module.exports = {
    send_to_chatbot
};

