import chatbot

bot = chatbot.Chatbot()
trading_date='2026-08-26'

# initialize the chatbot to have faster responses for the upcoming chats
bot.initialize_chatbot()

portfolio, portfolio_dict, st, gdict = bot.apply_strategy(trading_date=trading_date)

answer = bot.generate_advice(portfolio, portfolio_dict, trading_date)

print('\n', answer)