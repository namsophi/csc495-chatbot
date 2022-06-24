import random
from utils import listening
from keywords import BYE_ANSWER, YES_INPUT, YES_ANSWER, \
    NO_INPUT, NO_ANSWER, NEW_NAME_REMOVE_WORDS, NEW_NAME_INPUT


def hello_greeting(ai):
    ai.text_to_speech(f"Hello! Is this {ai.name}?")
    _greeting_response_handler(ai)


def bye_greeting(ai):
    ai.text_to_speech(random.choice(BYE_ANSWER) + ai.name)


def _greeting_response_handler(ai):
    response = listening(ai)
    if response is None:
        ai.text_to_speech("Oops! Didn't catch that")
        _greeting_response_handler(ai)
    # clas = ai.classifier.classify(
    #     ai.dialogue_act_features(response))
    # print(clas)
    # if clas == 'Accept' or clas == 'yAnswer':
    #     ai.text_to_speech(random.choice(YES_ANSWER) + ai.name)
    #     return
    # elif clas == 'Reject' or clas == 'nAnswer':
    #     ai.text_to_speech(random.choice(NO_ANSWER))
    #     ai.name = _new_name_listener(ai)
    #     ai.text_to_speech(f"Is your name {ai.name}?")
    #     _greeting_response_handler(ai)
    for word in response.split():
        if word.lower() in YES_INPUT:
            ai.text_to_speech(random.choice(YES_ANSWER) + ai.name)
            return
        elif word.lower() in NO_INPUT:
            ai.text_to_speech(random.choice(NO_ANSWER))
            ai.name = _new_name_listener(ai)
            ai.text_to_speech(f"Is your name {ai.name}?")
            _greeting_response_handler(ai)
    ai.text_to_speech("Oops! Didn't catch that")
    _greeting_response_handler(ai)


def _new_name_listener(ai):
    response = listening(ai)
    if response is None:
        ai.text_to_speech("Oops! Didn't catch that")
        ai.text_to_speech(random.choice(NO_ANSWER))
        _new_name_listener(ai)
    words = response.split()
    for word in words:
        if word.lower() in NEW_NAME_INPUT:
            new_name = [word for word in words
                        if word not in NEW_NAME_REMOVE_WORDS]
            return new_name
        elif len(words) == 1:
            return words[0]

