# import speech_recognition as sr
# import pyttsx3
# import os
# import webbrowser
# import pyautogui
# import schedule
# from plyer import notification
# from selenium import webdriver
# import openai
# import platform
# from datetime import datetime
# import json
# import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# ##


# # Initialize Text-to-Speech engine
# engine = pyttsx3.init()

# # Function to list and set available voices
# def set_jarvis_voice():
#     voices = engine.getProperty('voices')
#     # Set the voice to a female voice (you can change index for male/female voices)
#     engine.setProperty('voice', voices[1].id)  # Index 1 is usually female
#     engine.setProperty('rate', 150)  # Speed of speech
#     engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# def speak(text):
#     """Speak the given text using pyttsx3"""
#     engine.say(text)
#     engine.runAndWait()

# # Set Jarvis voice at startup
# set_jarvis_voice()

# def set_jarvis_voice(rate=150, volume=1.0):
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[0].id)  # Female voice
#     engine.setProperty('rate', rate)  # Speed of speech
#     engine.setProperty('volume', volume)  # Volume (0.0 to 1.0)

# ##

# # # Initialize Text-to-Speech engine
# # engine = pyttsx3.init()
# # engine.setProperty('rate', 150)  # Speed of speech
# # engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

# # def speak(text):
# #     """Speak the given text using pyttsx3"""
# #     engine.say(text)
# #     engine.runAndWait()

# def take_command():
#     """Take voice input from the user and return the recognized command"""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)
#     try:
#         print("Recognizing...")
#         command = recognizer.recognize_google(audio)
#         return command.lower()
#     except sr.UnknownValueError:
#         return "Sorry, I didn't understand that."

# #### Notification


# def notify_task_started(task):
#     """Show a notification for task start"""
#     notification.notify(
#         title="Task Started",
#         message=f"Starting task: {task}",
#         timeout=5  # Duration in seconds
#     )

# def notify_task_completed(task):
#     """Show a notification when the task is completed"""
#     notification.notify(
#         title="Task Completed",
#         message=f"Task {task} has been completed.",
#         timeout=5
#     )


# ####








# ### Notification command

# def execute_command(command):
#     """Execute commands based on user input"""
#     if "open browser" in command:
#         speak("Opening browser")
#         notify_task_started("Opening Browser")
#         webbrowser.open("https://www.google.com")
#         notify_task_completed("Opening Browser")
#     elif "search google for" in command:
#         query = command.replace("search google for", "").strip()
#         notify_task_started(f"Searching Google for {query}")
#         search_google(query)
#         notify_task_completed(f"Search Google for {query}")
#     elif "set reminder" in command:
#         task = command.replace("set reminder", "").strip()
#         schedule_task(task)
#         notify_task_started(f"Setting reminder for {task}")
#         schedule.every().day.at(time).do(reminder, task=task)
#         notify_task_completed(f"Reminder set for {task}")
#     # Add other command checks with notifications





# # @@@$$$$$$

# def execute_command(command):
#     """Execute commands based on user input"""
#     if "open browser" in command:
#         speak("Opening browser")
#         webbrowser.open("https://www.google.com")
#     elif "open file" in command:
#         speak("Opening file explorer")
#         os.system("explorer")
#     elif "shutdown" in command:
#         speak("Shutting down the system")
#         os.system("shutdown /s /t 1")
#     elif "search google for" in command:
#         query = command.replace("search google for", "").strip()
#         search_google(query)
#     elif "set reminder" in command:
#         task = command.replace("set reminder", "").strip()
#         schedule_task(task)
#     elif "open folder" in command:
#         path = command.replace("open folder", "").strip()
#         open_file(path)
#     elif "tell me the weather" in command:
#         get_weather()
#     elif "what is the time" in command:
#         tell_time()
#     elif "chat with ai" in command:
#         query = command.replace("chat with ai", "").strip()
#         response = chat_with_ai(query)
#         speak(response)
#     else:
#         speak("I can't perform that task yet.")

# # Google Search Automation
# # def search_google(query):
# #     """Search Google for the given query using Selenium"""
# #     driver = webdriver.Chrome(executable_path="path_to_chromedriver")
# #     driver.get(f"https://www.google.com/search?q={query}")



# def search_google(query):
#     # Set up ChromeDriver using the Service class
#     service = Service(ChromeDriverManager().install())  # Automatically installs ChromeDriver
#     driver = webdriver.Chrome(service=service)  # Pass the service object to the driver
    
#     driver.get(f"https://www.google.com/search?q={query}")
#     # Your code to handle the search results
#     # Don't forget to close the driver when done
#     driver.quit()


# # Reminder Setup
# def reminder(task):
#     """Display a desktop notification for the reminder"""
#     notification.notify(
#         title="Task Reminder",
#         message=f"Reminder: {task}",
#         timeout=10
#     )

# def schedule_task(task):
#     """Remind task at a specific time"""
#     speak("At what time should I remind you? For example, say 14:00.")
#     time = take_command()
#     schedule.every().day.at(time).do(reminder, task=task)
#     speak(f"Task scheduled for {time}.")

# # File/Folder Opening
# def open_file(path):
#     """Open a file or folder path using PyAutoGUI"""
#     pyautogui.hotkey('win', 'r')
#     pyautogui.typewrite(path)
#     pyautogui.press('enter')

# # Chat with OpenAI
# def chat_with_ai(prompt):
#     """Interact with OpenAI's GPT API for intelligent conversation"""
#     openai.api_key = "your-api-key"
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150
#     )
#     return response['choices'][0]['text'].strip()

# # Weather Information
# def get_weather():
#     """Fetch and speak the current weather using a weather API"""
#     api_key = "your-weather-api-key"
#     city = "your-city"
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         temp = data['main']['temp']
#         weather = data['weather'][0]['description']
#         speak(f"The current temperature in {city} is {temp} degrees Celsius with {weather}.")
#     else:
#         speak("I couldn't fetch the weather details right now.")

# # Time Information
# def tell_time():
#     """Tell the current system time"""
#     now = datetime.now()
#     current_time = now.strftime("%H:%M")
#     speak(f"The current time is {current_time}.")

# # Wake Word Detection (Placeholder for Snowboy or similar tools)
# def wake_word_detected():
#     """Simulate wake word detection"""
#     speak("I am ready to assist you!")
#     while True:
#         command = take_command()
#         if "exit" in command or "quit" in command or "band kro" in command:
#             speak("Goodbye!")
#             break
#         execute_command(command)

# # Main Function
# if __name__ == "__main__":
#     speak("Salaam! I am your AI Assistant Jarvis.")
#     # Wake word detection logic would go here (e.g., using Snowboy)
#     while True:
#         wake_word_detected()


# import speech_recognition as sr
# import pyttsx3
# import os
# import webbrowser
# import pyautogui
# import schedule
# from plyer import notification
# import openai
# import platform
# from datetime import datetime
# import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# # Initialize Text-to-Speech engine
# engine = pyttsx3.init()

# # Set up Jarvis voice (editable)
# def set_jarvis_voice(rate=150, volume=1.0):
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[0].id)  # Female voice (change index for male/female)
#     engine.setProperty('rate', rate)  # Speed of speech
#     engine.setProperty('volume', volume)  # Volume (0.0 to 1.0)

# def speak(text):
#     """Speak the given text using pyttsx3"""
#     engine.say(text)
#     engine.runAndWait()

# # Set Jarvis voice at startup
# set_jarvis_voice()

# def take_command():
#     """Take voice input from the user and return the recognized command"""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)
#     try:
#         print("Recognizing...")
#         command = recognizer.recognize_google(audio)
#         return command.lower()
#     except sr.UnknownValueError:
#         return "Sorry, I didn't understand that."

# def execute_command(command):
#     """Execute commands based on user input"""
#     if "open browser" in command:
#         speak("Opening browser")
#         webbrowser.open("https://www.google.com")
#         notify_task_started("Opening Browser")
#         notify_task_completed("Opening Browser")
#     elif "open file" in command:
#         speak("Opening file explorer")
#         os.system("explorer")
#         notify_task_started("Opening File Explorer")
#         notify_task_completed("Opening File Explorer")
#     elif "shutdown" in command:
#         speak("Shutting down the system")
#         os.system("shutdown /s /t 1")
#         notify_task_started("Shutdown")
#     elif "search google for" in command:
#         query = command.replace("search google for", "").strip()
#         search_google(query)
#     elif "set reminder" in command:
#         task = command.replace("set reminder", "").strip()
#         schedule_task(task)
#     elif "open folder" in command:
#         path = command.replace("open folder", "").strip()
#         open_file(path)
#     elif "tell me the weather" in command:
#         get_weather()
#     elif "what is the time" in command:
#         tell_time()
#     elif "chat with ai" in command:
#         query = command.replace("chat with ai", "").strip()
#         response = chat_with_ai(query)
#         speak(response)
#     else:
#         speak("I can't perform that task yet.")

# def notify_task_started(task):
#     """Show a notification for task start"""
#     notification.notify(
#         title="Task Started",
#         message=f"Starting task: {task}",
#         timeout=10
#     )

# def notify_task_completed(task):
#     """Show a notification when the task is completed"""
#     notification.notify(
#         title="Task Completed",
#         message=f"Task {task} has been completed.",
#         timeout=5
#     )

# # Google Search Automation
# def search_google(query):
#     # Set up ChromeDriver using the Service class
#     service = Service(ChromeDriverManager().install())  # Automatically installs ChromeDriver
#     driver = webdriver.Chrome(service=service)  # Pass the service object to the driver
#     driver.get(f"https://www.google.com/search?q={query}")
#     driver.quit()

# # Reminder Setup
# def reminder(task):
#     """Display a desktop notification for the reminder"""
#     notification.notify(
#         title="Task Reminder",
#         message=f"Reminder: {task}",
#         timeout=10
#     )

# def schedule_task(task):
#     """Remind task at a specific time"""
#     speak("At what time should I remind you? For example, say 14:00.")
#     time = take_command()
#     schedule.every().day.at(time).do(reminder, task=task)
#     speak(f"Task scheduled for {time}.")

# # File/Folder Opening
# def open_file(path):
#     """Open a file or folder path using PyAutoGUI"""
#     pyautogui.hotkey('win', 'r')
#     pyautogui.typewrite(path)
#     pyautogui.press('enter')

# # Chat with OpenAI
# def chat_with_ai(prompt):
#     """Interact with OpenAI's GPT API for intelligent conversation"""
#     openai.api_key = "your-api-key"
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150
#     )
#     return response['choices'][0]['text'].strip()

# # Weather Information
# def get_weather():
#     """Fetch and speak the current weather using a weather API"""
#     api_key = "your-weather-api-key"
#     city = "your-city"
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         temp = data['main']['temp']
#         weather = data['weather'][0]['description']
#         speak(f"The current temperature in {city} is {temp} degrees Celsius with {weather}.")
#     else:
#         speak("I couldn't fetch the weather details right now.")

# # Time Information
# def tell_time():
#     """Tell the current system time"""
#     now = datetime.now()
#     current_time = now.strftime("%H:%M")
#     speak(f"The current time is {current_time}.")

# # Wake Word Detection (Placeholder for Snowboy or similar tools)
# def wake_word_detected():
#     """Simulate wake word detection"""
#     speak("I am ready to assist you!")
#     while True:
#         command = take_command()
#         if "exit" in command or "quit" in command or "band kro" in command:
#             speak("Goodbye!")
#             break
#         execute_command(command)

# # Main Function
# if __name__ == "__main__":
#     speak("Salaam! I am your AI Assistant Jarvis.")
#     # Wake word detection logic would go here (e.g., using Snowboy)
#     while True:
#         wake_word_detected()
