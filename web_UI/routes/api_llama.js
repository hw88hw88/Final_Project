'use strict';

// 1. Update URL to llamafile's chat completion endpoint
const chatbot_url = 'http://localhost:8080/v1/chat/completions';

const send_to_chatbot = async (message_input) => {
    try {
        const response = await fetch(chatbot_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
            },
            body: JSON.stringify({
                // 2. Llamafile expects the "messages" array format
                model: "local-model", // llamafile usually ignores this, but it's good practice
                messages: [
                    {
                        role: message_input.sender,
                        content: message_input.message,
                    }
                ],
                stream: false, // Set to false so we get one full JSON response instead of a stream
                temperature: 0.7, // Optional: adjust creativity
            }),
        });

        if (!response.ok) {
            throw new Error(`Server status: ${response.status}`);
        }

        const data = await response.json();

        // 3. Extract the text from the OpenAI-compatible response format
        // The path is usually choices[0].message.content
        return data.choices[0].message.content;

    } catch (error) {
        console.error("Error calling llamafile:", error);
        throw error;
    }
};

// Export the functions so they can be imported by other JavaScript files.
module.exports = {
    send_to_chatbot
};
