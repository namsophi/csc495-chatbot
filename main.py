from gtts import gTTS
import speech_recognition as sr
import os
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('popular', quiet=True)
nltk.download('nps_chat', quiet=True)
nltk.download('punkt')
nltk.download('wordnet')


class ChatBot:
    def __init__(self, name):
        print("--- starting up", name, "---")
        self.name = name
        self.posts = nltk.corpus.nps_chat.xml_posts()[:10000]
        self.feature_sets = [(self.dialogue_act_features(post.text),
                              post.get('class')) for post in self.posts]
        self.size = int(len(self.feature_sets) * 0.1)
        self.train_set, self.test_set = self.feature_sets[self.size:], \
            self.feature_sets[:self.size]
        self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)

    # To Recognise input type as QUES.

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print("listening...")
            audio = recognizer.listen(mic)
        try:
            user_response = format(recognizer.recognize_google(audio))
            print("me --> ", user_response)
        except sr.UnknownValueError:
            ai.text_to_speech("Oops! Didn't catch that")
            pass
        clas = self.classifier.classify(
            self.dialogue_act_features(user_response))
        if clas != 'Bye':
            if clas == 'Emotion':
                ai.text_to_speech("You're welcome!")
                return False
        else:
            ai.text_to_speech("Bye! take care.")
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
    ai = ChatBot(name="maya")
    flag = True
    while flag:
        flag = ai.speech_to_text()
