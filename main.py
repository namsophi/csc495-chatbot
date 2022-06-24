from gtts import gTTS
import os
import nltk
import geocoder
from dadjokes import Dadjoke
from scripts.cyclingEncouragement import cycling_encouragement
from scripts.greeting import hello_greeting, bye_greeting
from scripts.weather import get_current_weather
from utils import listening
from keywords import BYE_INPUT
from states import States

nltk.download('popular', quiet=True)
nltk.download('nps_chat', quiet=True)
nltk.download('punkt')
nltk.download('wordnet')


class ChatBot:
    def __init__(self, name):
        print("--- starting up ---")
        self.name = name
        self.posts = nltk.corpus.nps_chat.xml_posts()[:10000]
        self.feature_sets = [(self.dialogue_act_features(post.text),
                              post.get('class')) for post in self.posts]
        self.size = int(len(self.feature_sets) * 0.1)
        self.train_set, self.test_set = self.feature_sets[self.size:], \
            self.feature_sets[:self.size]
        self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)
        self.state = States.NEUTRAL
        self.dad_joke = Dadjoke()

    def speech_to_text(self):
        if self.state != 1:
            if self.state == 2:
                cycling_encouragement(ai)
                return True
        user_response = listening(ai)
        if user_response is None:
            self.dad_joke = Dadjoke()
            ai.text_to_speech(self.dad_joke.joke)
            return True
        if "thanks" in user_response or "thank you" in user_response:
            ai.text_to_speech("You're welcome!")
            return
        for word in user_response.split():
            if word.lower() in BYE_INPUT:
                bye_greeting(ai)
                return False

    @staticmethod
    def text_to_speech(text):
        print("ai --> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("res.mp3")
        os.system("afplay res.mp3")
        os.remove("res.mp3")

    @staticmethod
    def dialogue_act_features(post):
        features = {}
        for word in nltk.word_tokenize(post):
            features['contains({})'.format(word.lower())] = True
        return features


if __name__ == "__main__":
    g = geocoder.ip('me')
    ai = ChatBot(name="Sophie")
    hello_greeting(ai)
    weather_statements = get_current_weather(lat=g.latlng[0], lon=g.latlng[1])
    for statement in weather_statements:
        ai.text_to_speech(statement)
    flag = True
    while flag:
        ai.state = int(input("Current state: ") or 1)
        flag = ai.speech_to_text()
