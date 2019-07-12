# Void
 Void is an auto replier on telegram that makes use of Telethon as well as Chatbotter
 1. Telethon
 2. ELIZA
 3. ChatterBot

`pip install -r requirements.txt`   

Learn how to get started with 
>[Telethon](https://towardsdatascience.com/introduction-to-the-telegram-api-b0cd220dbed2)    
>[ELIZA](https://www.smallsurething.com/implementing-the-famous-eliza-chatbot-in-python/)   
>[ChatterBot](https://github.com/gunthercox/ChatterBot)

ELIZA and ChatterBot was used so that the replies to come up with a better response. This program will first produce an ELIZA response,where if it doesn't match will activate the chatterbot for the response. A minimum 90% confidence has also been set to reduce any unrelated replies.     

The test.py allows you to test the bot created using python console.   
The main.py will allow you to connect to telegram where the incoming messages will be replied by Void to the user. It has been set to only reply to private chats and ignore groups messages.   
The dataset used is in the conversational.yml file. 
