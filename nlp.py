import pyttsx3
import speech_recognition as sr
import os
import pywhatkit
import wikipedia
import datetime
import webbrowser
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Initialize voice engine
engine = pyttsx3.init()

# Configure voice settings
def configure_voice():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Use male voice
    engine.setProperty('rate', 150)

configure_voice()

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen to user commands
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source)
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {command}")
        except Exception as e:
            print("Sorry, I didn't catch that. Please repeat.")
            return ""
        return command.lower()

# Process command with NLP
def process_command(command):
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    
    # Tokenize and remove stop words
    words = word_tokenize(command)
    filtered_words = [word for word in words if word not in stop_words]

    # Example of identifying intent
    if "open" in filtered_words and "file" in filtered_words:
        return "open_file", command.replace('open file', '').strip()
    elif "play" in filtered_words and "song" in filtered_words:
        return "play_song", command.replace('play song', '').strip()
    elif "search" in filtered_words:
        return "search", command.replace('search', '').strip()
    elif "time" in filtered_words:
        return "time", None
    elif "facebook" in filtered_words:
        return "open_facebook", None
    elif "shut" in filtered_words or "exit" in filtered_words:
        return "exit", None
    else:
        return "unknown", command

# Main JARVIS function
def jarvis():
    speak("Hello! I am JARVIS, your personal assistant. How can I help you?")
    while True:
        command = take_command()
        if not command:
            continue
        
        # Process the command using NLP
        intent, query = process_command(command)

        if intent == "exit":
            speak("Goodbye! Have a great day.")
            break
        elif intent == "open_file":
            file_path = f"E:\\{query}.txt"  # Path to E:\ drive
            try:
                os.startfile(file_path)
                speak(f"Opening file {query}")
            except FileNotFoundError:
                speak(f"Sorry, I could not find the file {query}")
        elif intent == "play_song":
            pywhatkit.playonyt(query)
            speak(f"Playing {query} on YouTube.")
        elif intent == "time":
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {current_time}.")
        elif intent == "search":
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(result)
        elif intent == "open_facebook":
            webbrowser.open("https://www.facebook.com")
            speak("Opening Facebook.")
        else:
            speak("I didn't understand that. Can you rephrase?")

# Run the assistant
if __name__ == "__main__":
    jarvis()
