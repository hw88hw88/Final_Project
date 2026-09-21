// The code of this file is for the chatting on the web page
// The code was written by the author (Student No.: 200212427 of the University of London) of the project, and was used on the website <howa.space> that was written and owned by the same author.

const query = document.getElementById('query');
const response = document.getElementById('response');
const enter_button = document.getElementById('enter');
const clear_button = document.getElementById('clear');

let sender = null;
// jobs = [{id: 1, timer: timer_object}, {id: 2, timer: timer_object}]
const jobs = [];
const server_msg = document.getElementById('server_msg');

try {
    const stop_timer = (timer) => {
        clearInterval(timer);
    };

    const update_status = async (job_id) => {
        try{
            const url = window.location.href + 'status?job_id=' + job_id;
            const result_msg = await fetch(url);
            const result_json = await result_msg.json();

            if (result_json.status == 'pending')
            {
                sender = result_json.sender;
                server_msg.innerHTML = "<p>" + result_json.text + "</p>";
                console.log('pending...job_id= ' + job_id);
            }
            else if (result_json.status == 'completed')
            {
                console.log('completed...job_id= ' + job_id);
                const message_element = document.createElement('p');
                message_element.innerHTML = "<b>Financial Assistant</b>:<br>" + result_json.text + "<br>";
                message_element.className = "response";
                message_element.style.width = "100%";
                message_element.style.padding = "1rem 1rem";
                message_element.style.borderWidth = "3px";
                message_element.style.borderStyle = "solid";
                message_element.style.borderColor = "#bc4749";
                message_element.style.borderRadius = "1rem";
                message_element.style.backgroundColor = "white";
                response.appendChild(message_element);
                sender = result_json.sender;
                server_msg.innerHTML = "";
                for (const j in jobs)
                {
                    if (jobs[j].id == job_id){
                        stop_timer(jobs[j].timer);
                        jobs.splice(j, 1)
                    }
                }
            }
            else
            {
                console.log('failed...job_id= ' + job_id);
                server_msg.innerHTML = `<p>Connection failed.<br>Please refresh the page.</p>`;
                for (const j in jobs)
                {
                    if (jobs[j].id == job_id){
                        stop_timer(jobs[j].timer);
                        jobs.splice(j, 1)
                    }
                }
            }
        }
        catch (ex)
        {
            console.log("Name (update_status): " + ex.name);
            console.log("Message: " + ex.message);
            server_msg.innerHTML = `<p>Connection failed.<br>Please refresh the page.</p>`;
            for (const j in jobs)
            {
                if (jobs[j].id == job_id){
                    stop_timer(jobs[j].timer);
                    jobs.splice(j, 1)
                }
            }
        }
    };
    const api_chatbot = async () => {
        try{
            const result_msg = await fetch(window.location.href, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json",
                },
                body: 
                    JSON.stringify(
                        {
                            'sender': sender,
                            'message': user_input
                        }
                    )                
            });
            const result_json = await result_msg.json();

            if (result_json.status == 'pending')
            {
                sender = result_json.sender;
                server_msg.innerHTML = "<p>" + result_json.text + " </p>";
                const my_timer = setInterval(() => update_status(result_json.job_id), 3000);
                jobs.push(
                    {
                        id: result_json.job_id, 
                        timer: my_timer
                    }
                );
            }
            // if result_json.status != 'pending', it must be 'failed'.
            else if(result_json.sender)
            {
                sender = result_json.sender;
                server_msg.innerHTML = "<p>" + toString(result_json.text) + "<br>You can refresh the page to start a session later.</p>";
            }
            else
            {
                server_msg.innerHTML = "<p>" + toString(result_json.text) + "<br>You can refresh the page to start a session later.</p>";
            }
        }
        catch (ex)
        {
            console.log("Name (api_chatbot): " + ex.name);
            console.log("Message: " + ex.message);
            server_msg.innerHTML = `<p>Connection failed.<br>Please refresh the page.</p>`;
        }
    };
    const user_enter = () => {
        let user_input = query.value;
        const message_element = document.createElement('p');
        message_element.innerHTML = "<b>You</b>:<br>" + user_input + "<br>";
        message_element.className = "query";
        message_element.style.padding = "1rem 1rem";
        message_element.style.width = "100%";
        message_element.style.textAlign = "right";
        message_element.style.borderWidth = "3px";
        message_element.style.borderStyle = "solid";
        message_element.style.borderColor = "#6a994e";
        message_element.style.borderRadius = "1rem";
        message_element.style.backgroundColor = "white";
        response.appendChild(message_element);
        // clear the user input box
        query.value = "";
        api_chatbot();
    };

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
        query.value = "";
    });

    module.exports = {
        stop_timer, update_status, user_enter
    }

} catch (error) {
    console.error('Error:', error);
}


