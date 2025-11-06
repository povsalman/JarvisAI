# JarvisAI

A Python-based virtual assistant that uses speech recognition and integrates with generative AI models to perform tasks and answer queries.

## Features

* **Wake Word Activation:** Listens for the "Jarvis" wake word to activate.
* **Speech Recognition:** Uses `speech_recognition` to capture and transcribe voice commands.
* **Text-to-Speech:** Responds vocally using either `pyttsx3` (offline) or `gTTS` (online, higher quality).
* **Command Processing:**
    * Opens websites (Google, YouTube, Instagram, etc.).
    * Plays music from a user-defined `musicLibrary.py` file.
    * Fetches and reads top news headlines from NewsAPI.
* **AI Integration:**
    * Optionally connects to Google Gemini or OpenAI (GPT-3.5) for general knowledge questions and conversational capabilities.
    * Prompts user at startup to enable AI and provide an API key.

## Requirements

This project requires Python 3.x.

### Dependencies

You must install the following Python packages. It is recommended to use a virtual environment.

```bash
pip install speechrecognition
pip install pyaudio
pip install setuptools
pip install spacy
pip install pyttsx3
pip install requests
pip install openai
pip install gtts
pip install pygame
pip install google-generativeai
```

**Note on `pyaudio`:** This package may have system-level dependencies (like PortAudio) depending on your operating system. If `pip install pyaudio` fails, please check its documentation for OS-specific installation instructions.

### Language Model

The project uses `spacy` for name extraction. You must download the required English model:

```bash
python -m spacy download en_core_web_sm
```

## Configuration

Before running the assistant, you need to configure API keys and the music library.

### 1. API Keys

This assistant relies on external APIs for news and AI.

  * **News API:**

    1.  Get a free API key from [newsapi.org](https://newsapi.org/).
    2.  In `main.py`, find the line `newsAPIKey = None` and replace `None` with your API key string.

  * **Google Gemini / OpenAI (Optional):**
    The script is designed to ask for your API key at runtime when you enable the AI feature. No hardcoding is required.

### 2. Music Library

The "play song" command depends on a local file named `musicLibrary.py`.

1.  Create a new file in the same directory named `musicLibrary.py`.

2.  Inside this file, create a dictionary named `music` that maps song titles (what you will say) to their web URLs (e.g., YouTube links).

    **Example `musicLibrary.py`:**

    ```python
    music = {
        "sad romance": "https://www.youtube.com/watch?v=example_link_1",
        "epic battle music": "https://www.youtube.com/watch?v=example_link_2"
    }
    ```

## Usage

1.  Ensure all dependencies are installed and configurations are set.
2.  Run the main script from your terminal:
    ```bash
    python main.py
    ```
3.  You will be asked if you want to enable AI. Type `y` or `n`.
4.  If you type `y`, paste your Google Gemini or OpenAI API key when prompted.
5.  The assistant will initialize and start "Listening...".
6.  Say the wake word "Jarvis" to activate it.
7.  Jarvis will respond "Ya" and listen for your command.
8.  Give a command, such as:
      * "Open Google"
      * "Play sad romance"
      * "What's in the news?"
      * (If AI is enabled) "What is the capital of Spain?"
