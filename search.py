import pyttsx3
import speech_recognition as sr
import os
import pywhatkit
import wikipedia
import datetime
import webbrowser

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

# Search files locally in a folder or drive
def search_files(query, search_path="E:\\"):
    matched_files = []
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if query.lower() in file.lower():
                matched_files.append(os.path.join(root, file))
    return matched_files

# Main JARVIS function
def jarvis():
    speak("Hello! I am JARVIS, your personal assistant. Welcome MOueen Togarvi. have ")
    while True:
        command = take_command()
        if not command:
            continue

        if 'exit' in command or 'shut down' in command:
            speak("Goodbye! Have a great day.")
            break

        # Online Wikipedia search
        elif 'search wikipedia' in command:
            query = command.replace('search wikipedia', '').strip()
            speak(f"Searching Wikipedia for {query}")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(result)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("The topic is too ambiguous. Try to be more specific.")
            except Exception:
                speak("Sorry, I couldn't find any information on Wikipedia.")

        # Google search
        elif 'search google' in command:
            query = command.replace('search google', '').strip()
            speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")

        # Offline file search
        elif 'search file' in command:
            query = command.replace('search file', '').strip()
            speak(f"Searching for files containing {query} in the E drive.")
            results = search_files(query)
            if results:
                speak(f"I found {len(results)} file(s). Opening the first one.")
                os.startfile(results[0])
            else:
                speak("No files found with that name.")

        # Play song on YouTube
        elif 'play' in command:
            query = command.replace('play', '').strip()
            speak(f"Playing {query} on YouTube.")
            pywhatkit.playonyt(query)

        # Current time
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {current_time}.")

        # Open Facebook
        elif 'open facebook' in command:
            webbrowser.open("https://www.facebook.com")
            speak("Opening Facebook.")

        else:
            speak("I didn't understand that. Can you rephrase?")

# Run the assistant
if __name__ == "__main__":
    jarvis()
