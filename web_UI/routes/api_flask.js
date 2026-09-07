'use strict';

const chatbot_url = 'http://localhost:5000';

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
                    'sender': message_input.sender,
                    'message': message_input.message,
                }
            ),
    });

    if (!response.ok)
    {
        throw new Error(`Server status: ` + response.status);
    }

    return await response.json();
    const result = json.text;
    return result;

};

// Export the functions so they can be imported by other JavaScript files.
module.exports = {
    send_to_chatbot
};

