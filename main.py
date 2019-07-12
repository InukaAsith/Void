import time

from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendMessageRequest
import telethon.sync

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

import re
import random

reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

psychobabble = [
    [r'I need (.*)',
     ["Why do you need {0}?",
      "Would it really help you to get {0}?",
      "Are you sure you need {0}?"]],

    [r'Why don\'?t you ([^\?]*)\??',
     ["Do you really think I don't {0}?",
      "Perhaps eventually I will {0}.",
      "Do you really want me to {0}?"]],

    [r'Why can\'?t I ([^\?]*)\??',
     ["Do you think you should be able to {0}?",
      "If you could {0}, what would you do?",
      "I don't know -- why can't you {0}?",
      "Have you really tried?"]],

    [r'I can\'?t (.*)',
     ["How do you know you can't {0}?",
      "Perhaps you could {0} if you tried.",
      "What would it take for you to {0}?"]],

    [r'I am (.*)',
     ["Did you come to me because you are {0}?",
      "How long have you been {0}?",
      "How do you feel about being {0}?"]],

    [r'I\'?m (.*)',
     ["How does being {0} make you feel?",
      "Do you enjoy being {0}?",
      "Why do you tell me you're {0}?",
      "Why do you think you're {0}?"]],

    [r'Are you ([^\?]*)\??',
     ["Why does it matter whether I am {0}?",
      "Would you prefer it if I were not {0}?",
      "Perhaps you believe I am {0}.",
      "I may be {0} -- what do you think?"]],

    [r'What (.*)',
     ["Why do you ask?",
      "How would an answer to that help you?",
      "What do you think?"]],

    [r'How (.*)',
     ["How do you suppose?",
      "Perhaps you can answer your own question.",
      "What is it you're really asking?"]],

    [r'Because (.*)',
     ["Is that the real reason?",
      "What other reasons come to mind?",
      "Does that reason apply to anything else?",
      "If {0}, what else must be true?"]],

    [r'(.*) sorry (.*)',
     ["There are many times when no apology is needed.",
      "What feelings do you have when you apologize?"]],

    [r'Hello(.*)',
     ["Hello, you good?",
      "Hi there, how are you today?",
      "Hello, how are you feeling today?"]],

    [r'I think (.*)',
     ["Do you doubt {0}?",
      "Do you really think so?",
      "But you're not sure {0}?"]],

    [r'(.*) friend (.*)',
     ["Tell me more about your friends.",
      "When you think of a friend, what comes to mind?",
      "Why don't you tell me about a childhood friend?"]],

    [r'Yes',
     ["You seem quite sure.",
      "OK, but can you elaborate a bit?"]],

    [r'(.*) computer(.*)',
     ["Are you really talking about me?",
      "Does it seem strange to talk to a computer?",
      "How do computers make you feel?",
      "Do you feel threatened by computers?"]],

    [r'Is it (.*)',
     ["Do you think it is {0}?",
      "Perhaps it's {0} -- what do you think?",
      "If it were {0}, what would you do?",
      "It could well be that {0}."]],

    [r'It is (.*)',
     ["You seem very certain.",
      "If I told you that it probably isn't {0}, what would you feel?"]],

    [r'Can you ([^\?]*)\??',
     ["What makes you think I can't {0}?",
      "If I could {0}, then what?",
      "Why do you ask if I can {0}?"]],

    [r'Can I ([^\?]*)\??',
     ["Perhaps you don't want to {0}.",
      "Do you want to be able to {0}?",
      "If you could {0}, would you?"]],

    [r'You are (.*)',
     ["Why do you think I am {0}?",
      "Does it please you to think that I'm {0}?",
      "Perhaps you would like me to be {0}.",
      "Perhaps you're really talking about yourself?"]],

    [r'You\'?re (.*)',
     ["Why do you say I am {0}?",
      "Why do you think I am {0}?",
      "Are we talking about you, or me?"]],

    [r'I don\'?t (.*)',
     ["Don't you really {0}?",
      "Why don't you {0}?",
      "Do you want to {0}?"]],

    [r'I feel (.*)',
     ["Good, tell me more about these feelings.",
      "Do you often feel {0}?",
      "When do you usually feel {0}?",
      "When you feel {0}, what do you do?"]],

    [r'I have (.*)',
     ["Why do you tell me that you've {0}?",
      "Have you really {0}?",
      "Now that you have {0}, what will you do next?"]],

    [r'I would (.*)',
     ["Could you explain why you would {0}?",
      "Why would you {0}?",
      "Who else knows that you would {0}?"]],

    [r'Is there (.*)',
     ["Do you think there is {0}?",
      "It's likely that there is {0}.",
      "Would you like there to be {0}?"]],

    [r'My (.*)',
     ["I see, your {0}.",
      "Why do you say that your {0}?",
      "When your {0}, how do you feel?"]],

    [r'You (.*)',
     ["We should be discussing you, not me.",
      "Why do you say that about me?",
      "Why do you care whether I {0}?"]],

    [r'Why (.*)',
     ["Why don't you tell me the reason why {0}?",
      "Why do you think {0}?"]],

    [r'(.*) sleep',
     ["Nitez",
      "GoodNitez",
      "Go sleep"]],
    [r'(.*) ice bear',
     ["thats me haha",
      "i am ice bear",
      "yeeet"]],

    [r'I want (.*)',
     ["What would it mean to you if you got {0}?",
      "Why do you want {0}?",
      "What would you do if you got {0}?",
      "If you got {0}, then what would you do?"]],

    [r'(.*)\?',
     ["Why do you ask that?",
      "Please consider whether you can answer your own question.",
      "Perhaps the answer lies within yourself?",
      "Why don't you tell me?"]],

    [r'quit',  # In ELIZA, if you typed 'quit' these would print and the script would end.
     ["Thank you for talking with me.",
      "Good-bye.",
      "Thank you, that will be $150.  Have a good day!"]],
]

# Declare Bot
english_bot = ChatBot("Void",
                      storage_adapter="chatterbot.storage.SQLStorageAdapter",
                      logic_adapters=[
                          {
                              'import_path': 'chatterbot.logic.BestMatch',
                              'default_response': 'I am sorry, let me get back to you later.',
                              'maximum_similarity_threshold': 0.90
                          }
                      ])

trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("C:\\Users\\Jeremy John\\Desktop\\Telegram Bot Bob\\conversations.yml")

# sample API_ID from https://github.com/telegramdesktop/tdesktop/blob/f98fdeab3fb2ba6f55daf8481595f879729d1b84/Telegram/SourceFiles/config.h#L220
# or use your own
api_id = TG_API_ID
api_hash = TG_API_HASH

# fill in your own details here
phone = ''
session_file = ''  # use your username if unsure
password = ''  # if you have two-step verification enabled

# content of the automatic reply
# message = "How can I help you ? "


def reflect(fragment):  # These have to be here...
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


def analyze(statement):  # ...to define analyze for the greeting.
    for pattern, responses in psychobabble:
        match = re.match(pattern, str(statement))
        if match:
            rspns = random.choice(responses)
            return rspns.format(*[reflect(g) for g in match.groups()])


def get_bot_response(userText):

    def reflect(userText):
        tokens = userText.lower().split()
        for i, token in enumerate(tokens):
            if token in reflections:
                tokens[i] = reflections[token]
        return ' '.join(tokens)

    def analyze(userText):
        for pattern, responses in psychobabble:
            match = re.match(pattern, str(userText))
            if match:  # ELIZA Responses
                rspns = random.choice(responses)
                return rspns.format(*[reflect(g) for g in match.groups()])
        else:  # ChatterBot Responses
            response = english_bot.get_response(userText)
            return response
    # return str(english_bot.get_response(userText))
    return str(analyze(userText))


if __name__ == '__main__':
    # Create the client and connect
    # use sequential_updates=True to respond to messages one at a time
    client = TelegramClient(session_file, api_id,
                            api_hash, sequential_updates=True)

    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):
        # print(event.message.message)
        if event.is_private:  # only auto-reply to private chats
            # this lookup will be cached by telethon
            from_ = await event.client.get_entity(event.from_id)
            # print("UserID = "+event.from_id)
            if not from_.bot:  # don't auto-reply to bots
                # print(event.message.message)
                # print(get_bot_response(event.message.message))
                # for x in blacklist:
                #     if x == event.from_id:
                await event.respond(("Void: \n" + get_bot_response(event.message.message)))

    print(time.asctime(), '-', 'Auto-replying...')
    client.start(phone, password)
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stopped!')
