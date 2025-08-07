import sounddevice as sd
import scipy.io.wavfile
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def record_audio(filename="output.wav", duration=5, fs=44100):
    speak("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    scipy.io.wavfile.write(filename, fs, audio)
    return filename

def transcribe_audio(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data).lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Speech service is unavailable.")
        return ""

def respond(command):
    if "hello" in command:
        speak("Hello! How can I help you?")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
    elif "date" in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")
    elif "search for" in command:
        query = command.split("search for")[-1].strip()
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I didn't understand that.")

if __name__ == "__main__":
    speak("Voice assistant ready.")
    while True:
        filename = record_audio()
        command = transcribe_audio(filename)
        if command:
            respond(command)
