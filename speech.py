import speech_recognition as sr

def asrGoogle(msg = "Say something!"):
# obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(msg)
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        return str(r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
