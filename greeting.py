import random

import speech_recognition as sr

BYE_ANSWER = ["Bye ", "Nice talking to you, ", "See you soon, "]
YES_ANSWER = ["Hey good to talk to you, ", "hello, ", "Good to see you, "]
YES_INPUT = ["yes", "yeah", "yep", "yup"]
NO_ANSWER = ["could you tell me your name again?", "tell me your name!",
             "what's your name?"]
NO_INPUT = ["no", "nope", "not"]
NEW_NAME_INPUT = ["my name is", "it is", "I am", "the name is"]
NEW_NAME_REMOVE_WORDS = ["my", "name", "is", "it", "I", "am", "the", "name"]


def hello_greeting(ai):
    ai.text_to_speech(f"Hello! Is this {ai.name}?")
    _greeting_response_handler(ai)


def bye_greeting(ai):
    ai.text_to_speech(random.choice(BYE_ANSWER) + ai.name)


def _greeting_response_handler(ai):
    response = _listening(ai)
    for word in response.split():
        if word.lower() in YES_INPUT:
            ai.text_to_speech(random.choice(YES_ANSWER) + ai.name)
        elif word.lower() in NO_INPUT:
            ai.text_to_speech(random.choice(NO_ANSWER) + ai.name)
            ai.name = _new_name_listener(ai)


def _new_name_listener(ai):
    response = _listening(ai)
    words = response.split()
    for word in words:
        if word.lower() in NEW_NAME_INPUT:
            new_name = [word for word in words
                        if word not in NEW_NAME_REMOVE_WORDS]
            return new_name
        elif len(words) == 1:
            return words[0]


def _listening(ai):
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print("listening...")
        audio = recognizer.listen(mic)
    try:
        user_response = format(recognizer.recognize_google(audio))
        print("me --> ", user_response)
    except sr.UnknownValueError:
        ai.text_to_speech("Oops! Didn't catch that")
        _listening(ai)
    return user_response
