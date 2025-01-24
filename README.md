
# JARVIS: Your Personal AI Assistant

This project is a Python-based virtual assistant named JARVIS. It uses voice commands to interact with users and perform a variety of tasks, such as answering queries, searching the web, playing YouTube videos, managing system settings, and more.

## Features
- **Speech Recognition**: Recognizes voice commands using `speech_recognition`.
- **Text-to-Speech Output**: Converts text to speech using `pyttsx3`.
- **Search and Play**: Searches Google, Wikipedia, and plays YouTube videos.
- **System Control**: Adjust system volume, shut down, or restart the computer.
- **Customizable AI Responses**: Leverages Gemini AI for intelligent replies.
- **Application/Website Launcher**: Opens installed applications or websites.

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

### Step 2: Create a Virtual Environment
```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment
- On Windows:
  ```bash
  .venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
- Create a `.env` file in the root directory and add your Gemini API key:
  ```
  GEMINI_API_KEY=your_api_key_here
  ```

## Usage

### Step 1: Run the Script
```bash
python jarvis.py
```

### Step 2: Give Voice Commands
Once the assistant is running, you can use the following commands:
- **"What is the time?"** – Tells the current time.
- **"Search Wikipedia [query]"** – Searches Wikipedia and reads the summary.
- **"Search Google [query]"** – Opens Google search for the query.
- **"Set volume to [0-100]"** – Adjusts the system volume.
- **"Open [application or website]"** – Opens an application or website.
- **"Shutdown system"** – Shuts down the system.
- **"Play [song] on YouTube"** – Plays the specified song on YouTube.
- **"Exit"** – Exits the assistant.

## Libraries Used
1. **[pyttsx3](https://pyttsx3.readthedocs.io/en/latest/)**: Text-to-speech conversion.
2. **[speech_recognition](https://pypi.org/project/SpeechRecognition/)**: Speech recognition for capturing voice commands.
3. **[wikipedia](https://pypi.org/project/wikipedia/)**: Wikipedia search.
4. **[pywhatkit](https://pypi.org/project/pywhatkit/)**: YouTube playback.
5. **[pycaw](https://pycaw.readthedocs.io/en/latest/)**: Audio control for system volume.
6. **[dotenv](https://pypi.org/project/python-dotenv/)**: Manage environment variables.
7. **[requests](https://docs.python-requests.org/en/master/)**: API calls to Gemini AI.

## API Integration
The project integrates with OpenAI's Gemini AI model for intelligent responses. The API is called using the `ask_ai()` function, which sends a request and parses the response.

### Example:
```python
question = "Explain how AI works"
response = ask_ai(question)
print(response)
```

## How It Works
1. **Voice Input**: The assistant listens for user input via a microphone.
2. **Command Parsing**: Commands are processed to determine the appropriate action.
3. **Execution**: Based on the command, the assistant executes tasks like fetching search results, controlling system settings, or interacting with AI APIs.
4. **Voice Feedback**: Outputs results or confirmations via speech.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any feature enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
This project was inspired by the capabilities of AI-powered virtual assistants and is made possible by:
- OpenAI
- Python community

---
Enjoy using JARVIS, your personal AI assistant!