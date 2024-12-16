import pyttsx3
import speech_recognition as sr
import os
import pywhatkit
import wikipedia
import datetime
import webbrowser
import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet

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
        speak("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source)
            speak("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {command}")
        except sr.RequestError:
            speak("Unable to connect to the recognition service. Check your internet.")
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that. Please repeat.")
            return ""
        return command.lower()

# IoT MQTT Configuration
MQTT_BROKER = "broker.hivemq.com"  # Public MQTT Broker
MQTT_PORT = 1883
MQTT_TOPIC = "home/commands"

client = mqtt.Client()

def connect_to_mqtt():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        print("Connected to MQTT broker.")
    except Exception as e:
        print(f"MQTT connection failed: {e}")
        speak("Unable to connect to the IoT server.")

def control_iot_device(command):
    if "turn on light" in command:
        client.publish(MQTT_TOPIC, "light:on")
        speak("Turning on the light.")
    elif "turn off light" in command:
        client.publish(MQTT_TOPIC, "light:off")
        speak("Turning off the light.")
    elif "set thermostat" in command:
        temp = command.replace("set thermostat to", "").strip()
        client.publish(MQTT_TOPIC, f"thermostat:{temp}")
        speak(f"Setting the thermostat to {temp} degrees.")
    else:
        speak("I couldn't recognize the device command.")

# Security Features: Encryption
KEY = Fernet.generate_key()
cipher_suite = Fernet(KEY)

def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data).decode()

# Save credentials securely
def save_credentials(service, credentials):
    encrypted_credentials = encrypt_data(credentials)
    with open(f"{service}_credentials.enc", "wb") as file:
        file.write(encrypted_credentials)

def load_credentials(service):
    try:
        with open(f"{service}_credentials.enc", "rb") as file:
            encrypted_credentials = file.read()
        return decrypt_data(encrypted_credentials)
    except FileNotFoundError:
        return None

# Voice Authentication Placeholder
AUTHORIZED_VOICE = "YourAuthorizedVoiceSignature"

def authenticate_voice():
    # Placeholder for actual voice authentication logic
    return True  # Simulated successful authentication

# Command Execution
def execute_command(command):
    if "turn on light" in command or "turn off light" in command or "set thermostat" in command:
        control_iot_device(command)
    elif "time" in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {current_time}.")
    elif "search wikipedia" in command:
        query = command.replace("search wikipedia", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia: {result}")
        except Exception:
            speak("I couldn't find anything on Wikipedia.")
    elif "search google" in command:
        query = command.replace("search google", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}.")
    elif "play" in command:
        query = command.replace("play", "").strip()
        try:
            pywhatkit.playonyt(query)
            speak(f"Playing {query} on YouTube.")
        except Exception:
            speak("There was an issue playing the requested song.")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit(0)
    else:
        speak("I didn't understand that command. Please try again.")

# Main Function
def jarvis():
    connect_to_mqtt()
    if authenticate_voice():
        speak("Hello! I am JARVIS. How can I help you?")
        while True:
            command = take_command()
            if command:
                execute_command(command)
    else:
        speak("Authentication failed. Access denied.")

# Start the Assistant
if __name__ == "__main__":
    try:
        jarvis()
    except KeyboardInterrupt:
        speak("Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Something went wrong. Please try again later.")
