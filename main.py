from gtts import gTTS
import speech_recognition as sr
import numpy as np
import os


class ChatBot():
    def __init__(self, name):
        print("--- starting up", name, "---")
        self.name = name

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("listening...")
            audio = recognizer.listen(mic)
        try:
            self.text = recognizer.recognize_google(audio)
            print("me --> ", self.text)
        except:
            print("me -->  ERROR")

    def wake_up(self, text):
        return True if self.name in text.lower() else False

    @staticmethod
    def text_to_speech(text):
        print("ai --> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("res.mp3")
        os.system("afplay res.mp3")  # macbook->afplay | windows->start
        os.remove("res.mp3")


if __name__ == "__main__":
    ai = ChatBot(name="maya")

    while True:
        ai.speech_to_text()

        if ai.wake_up(ai.text) is True:
            res = "Hello I am Maya the AI, what can I do for you?"

        elif any(i in ai.text for i in ["thank","thanks"]):
            res = np.random.choice(["you're welcome!","anytime!","no problem!","cool!","I'm here if you need me!","peace out!"])

        ai.text_to_speech(res)
