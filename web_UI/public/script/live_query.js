// The code of this file is for the chatting on the web page
// The code was written by the author (Student No.: 200212427 of the University of London) of the project, and was used on the website <howa.space> that was written and owned by the same author.

const query = document.getElementById('query');
const response = document.getElementById('response');
const enter_button = document.getElementById('enter');
const clear_button = document.getElementById('clear');

const sender = document.getElementById('sender');

try {
    const user_enter = () => {
        let user_input = query.value;
        const messageElement = document.createElement('p');
        messageElement.innerHTML = "<b>You</b>:<br>" + user_input;
        messageElement.className = "query";
        response.appendChild(messageElement);
        // clear the user input box
        query.value = "";

        const api_chatbot = async () => {
            if (sender.value == undefined)
            {
                sender.value = Date.now();
            }
            const result_msg = await fetch(window.location.href, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json",
                },
                body: 
                    JSON.stringify(
                        {
                            'sender': sender.value,
                            'message': user_input
                        }
                    )                
            });

            if (!result_msg.ok)
            {
                const messageElement = document.createElement('p');
                messageElement.innerHTML = "<b>System</b>:<br>" + `Web server status: ` + result_msg.status;
                messageElement.className = "response";
                response.appendChild(messageElement);
                sender.value = json.sender;
            }
            else
            {
                const json = await result_msg.json();
                console.log(JSON.stringify(json));
                const result_message = json.text;

                const messageElement = document.createElement('p');
                messageElement.innerHTML = "<b>Chatbot</b>:<br>" + result_message;
                messageElement.className = "response";
                response.appendChild(messageElement);
                sender.value = json.sender;
            }
        };
        api_chatbot();
    }

    enter_button.addEventListener('mouseup', () => {
        user_enter();
    });

    window.addEventListener("keyup", (event) => {
        if(event.key == "Enter") {
            if (!event.shiftKey)
                user_enter();
        }
    });

    clear_button.addEventListener('mouseup', () => {
        response.innerHTML = "";
        query.value = "";
    });

} catch (error) {
    console.error('Error:', error);
}

