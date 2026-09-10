# import and initialize the chatbot and LLM
from chatbot import Chatbot
bot = Chatbot()
bot.initialize_chatbot()
import datetime

# import flask for the API server
from flask import Flask, request
app = Flask(__name__)

user_background = {}

@app.route('/', methods=['GET', 'POST'])
def chatbot_api():
    try:
        if request.method == 'GET':
            return {'text': 'This is chatbot API. Please use "POST" method.'}, 200

        data = request.get_json()
        
        if not data:
            return {'error': 'JSON missing'}, 400

        sender = data.get('sender')
        message = data.get('message')

        print('sender= ', sender)

        # generate new sender id for new users/ senders
        if not sender:
            sender = str(datetime.datetime.now())
            sender = sender.replace(' ', '_')
            sender = sender.replace(':', '-')

        print('\nidentifying user input')
        # understanding the prompt
        user_prompt_dict = bot.identify_user_input(
            user_prompt=message
        )

        # saving or updating user background
        if user_background.get(sender):
            # "greeting": false, "investment": true, "investment_explanation": false, "prefer_low_risk": false, "investment_date": null
            # investment
            ## investment is true if the same user expressed investment intent in the previous prompts
            if user_prompt_dict.get('investment') or user_prompt_dict.get('prefer_low_risk') is not None:
                user_background[sender]['investment'] = True
            # investment explanation
            ## investment explanation is true if the same user expressed investment explanation intent in the previous prompts
            if user_prompt_dict.get('investment_explanation'):
                user_background[sender]['investment_explanation'] = user_prompt_dict.get('investment_explanation')
            # prefer_low_risk
            ## prefer_low_risk in the previous prompts will be used if the preference in the latest prompt is none
            if user_prompt_dict.get('prefer_low_risk') != user_background.get(sender).get('prefer_low_risk'):
                if user_prompt_dict.get('prefer_low_risk') is not None:
                    user_background[sender]['prefer_low_risk'] = user_prompt_dict.get('prefer_low_risk')
            if user_prompt_dict.get('investment_date'):
                user_background[sender]['investment_date'] = user_prompt_dict.get('investment_date')

        else:
            user_background[sender] = user_prompt_dict

        print('\nclassifying response')
        # classifying the prompt into categories
        prompt = bot.classify_response(
            user_prompt_dict=user_background[sender],
            run_id_file_path = 'CSV/run_id.csv'
        )

        print('\ngenerating response')
        chatbot_response = bot.generate_response(
            prompt=prompt
        )
        print('\nreturning...')
        return (
            {
                'sender' : sender,
                'text': chatbot_response,
            }
        ), 200

    except Exception as e:
        print('Error: ', e)
        return ({'error': str(e)}), 500
