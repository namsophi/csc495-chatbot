import speech_recognition as sr


def listening(ai):
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print("listening...")
        try:
            audio = recognizer.listen(mic, timeout=5)
        except sr.WaitTimeoutError:
            return
    try:
        user_response = format(recognizer.recognize_google(audio))
        print("me --> ", user_response)
        return user_response
    except sr.UnknownValueError:
        ai.text_to_speech("Oops! Didn't catch that")
        listening(ai)
