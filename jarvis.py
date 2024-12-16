import pyttsx3
import speech_recognition as sr
import os
import pywhatkit
import wikipedia
import datetime
import webbrowser

# Initialize the voice engine
engine = pyttsx3.init()

# Configure voice settings
def configure_voice():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Use male voice
    engine.setProperty('rate', 150)  # Set speech rate

configure_voice()

# Function to make JARVIS speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user commands
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

# Main function for JARVIS
def jarvis():
    speak("Hello! I am JARVIS, your personal assistant. How can I help you?")
    while True:
        command = take_command()

        # Exit the assistant
        if 'shut down' in command or 'exit' in command:
            speak("Goodbye! Have a great day.")
            break

        # Open a specific file
        elif 'open file' in command:
            file_path = "C:\\Users\\YourUserName\\Documents\\example.txt"  # Update with your file path
            os.startfile(file_path)
            speak("Opening the file.")

        # Play a song on YouTube
        elif 'play song' in command:
            song = command.replace('play song', '')
            pywhatkit.playonyt(song)
            speak(f"Playing {song} on YouTube.")

        # Tell the current time
        elif 'what time is it' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The current time is {current_time}.")

        # Search Wikipedia
        elif 'search' in command:
            query = command.replace('search', '')
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(result)

        # Open social media platforms
        elif 'open facebook' in command:
            webbrowser.open("https://www.facebook.com")
            speak("Opening Facebook.")
        elif 'open instagram' in command:
            webbrowser.open("https://www.instagram.com")
            speak("Opening Instagram.")
        elif 'open twitter' in command:
            webbrowser.open("https://www.twitter.com")
            speak("Opening Twitter.")

        # Open browser
        elif 'open browser' in command:
            webbrowser.open("https://www.google.com")
            speak("Opening browser.")

        # General message for unsupported commands
        else:
            speak("I didn't understand that command. Can you repeat?")

# Run the assistant
if __name__ == "__main__":
    jarvis()
