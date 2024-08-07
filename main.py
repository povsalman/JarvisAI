# major pip install used are:
# 1) speechrecognition
# 2) pyaudio
# 3) setuptools
# 4) pip install -U spacy
#    python -m spacy download en_core_web_sm
# 5) webbrowser
# 6) pyttsx3
# 7) requests
# 8) openai
# 9) gtts
# 10) pygame
# 11) google-generativeai


import speech_recognition as sr  # To hear audio from Microphone
import spacy  # NLP for name recognition
import webbrowser  # opening/closing native browser tabs
import pyttsx3 as pt  # Default speak voice
import requests  # for requesting data from the web i.e. for news headlines
from openai import OpenAI  # For OpenAI integration (paid feature + requires personal API)
from gtts import gTTS  # For voice changing feature of speak function (paid)
import pygame  # For gtts, playing the speak function
import musicLibrary  # own file for adding music
import google.generativeai as genai  # gemini
import re  # removing *," " in gemini request
import os

# initializing
ttsx = pt.init()
nlp = spacy.load("en_core_web_sm")
newsAPIKey = None   # API KEY MUST BE PROVIDED IN REAL TIME


# To choose desired speak functionality, rename that function to "speak"

# unpaid pyttsx3 speak function
def speak_old(text):
    ttsx.say(text)
    ttsx.runAndWait()


# paid gtts speak function that uses pygame
def speak(text):
    # Create gTTS object with text and language ('en' for English)
    tts = gTTS(text=text, lang='en')

    # Save the speech to a temporary MP3 file
    tts.save("speech.mp3")

    # Initialize pygame mixer for audio playback
    pygame.mixer.init()

    # Load the saved MP3 file
    pygame.mixer.music.load("speech.mp3")

    # Play the loaded MP3 file
    pygame.mixer.music.play()

    # Wait until the speech finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up pygame mixer resources
    pygame.mixer.quit()


def extract_names(text):
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return names


# Optional AI Feature
# API KEY MUST BE PROVIDED IN REAL TIME
def ai_openai(iscommand, openai_user_apikey=None):
    # defaults to getting the key using os.environ.get("OPENAI_API_KEY")

    client = OpenAI(
        api_key=openai_user_apikey,
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Cloud.Give short responses"},
            {"role": "user", "content": iscommand}
        ]
    )

    return completion.choices[0].message.content


# api gemini
# API KEY MUST BE PROVIDED IN REAL TIME

def ai_gemini(iscommand, gemini_user_apikey=None):
    # Check if the API key is provided
    if gemini_user_apikey is None:
        raise ValueError("API key must be provided")

    # Configure the API key
    genai.configure(api_key=gemini_user_apikey)

    # Create the model with generation config
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 50,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Start a chat session with an initial user message
    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": [iscommand]}
        ]
    )

    # Send a message and get a response
    response = chat_session.send_message({"role": "user", "parts": [iscommand]})

    # Process the response text to remove asterisks
    clean_text = re.sub(r'\*+', '', response.text)

    return clean_text


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "open google classroom" in c.lower():
        webbrowser.open("https://classroom.google.com/")

    elif "play" in c.lower():
        words = c.lower().split(" ")  # Split the string into a list of words
        # Filter out "play" and "song" and join the rest
        song = " ".join([item for item in words if item != "play" and item != "song"])
        print(song)

        # Access the dictionary correctly
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            print(f"Sorry, the song '{song}' is not in the music library.")

    elif "news" in c.lower():
        req = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsAPIKey}")

        # Check if the request was successful (status code 200 means OK)
        if req.status_code == 200:
            # Parse the JSON response
            data = req.json()
            # Get the list of articles from the response
            articles = data.get("articles", [])
            # Iterate through each article in the list
            for article in articles:
                # Get the title of the article
                headlines = article.get("title")
                # Print the title if it exists
                if headlines:
                    print(headlines)
                    speak(headlines)
        else:
            # Print an error message if the request failed
            print("Failed to retrieve news")

    else:
        # Letting OpenAi to handle the request (optional)
        if openai_enabled:  # enabled
            # output = ai_openai(c, user_openai_key)
            print(c)
            output = ai_gemini(c, user_openai_key)
            print(output)
            speak(output)

        else:  # disabled
            pass


if __name__ == "__main__":

    speak("Initializing Jarvis.....")

    name_asked = True  # default: False
    active = True  # default: False
    openai_enabled = False  # default: False
    uname = []

    op = str(input("Do you want to enable OpenAI with Jarvis? (y/n) "))
    if "y" in op.lower():
        openai_enabled = True
        user_openai_key = str(input("Enter your OpenAI API Key: "))

    while True:
        # initializer
        r = sr.Recognizer()

        # recognize speech using Google Speech Recognition
        print("Recognizing...")
        try:
            # Listen for the wake word "Jarvis" using microphone
            with sr.Microphone() as source:
                print("Listening.....")
                r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                audio = r.listen(source, timeout=2, phrase_time_limit=1)  # listens for 2 seconds only

            word = r.recognize_google(audio)

            # Wake up command
            if "jarvis" in word.lower():

                speak("Ya")
                active = True

                # This loop now runs when Jarvis is activated once
                while active:

                    try:

                        if not name_asked:
                            speak("Who's there?")

                            with sr.Microphone() as source:
                                print("Listening for name...")
                                r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                                uname_audio = r.listen(source, timeout=2)
                                uname_str = r.recognize_google(uname_audio)

                            uname = extract_names(uname_str)
                            print(f"Hello, {', '.join(uname)}")
                            if uname:
                                speak(f"Hello {', '.join(uname)}")
                                speak("How can I assist you?")
                            else:
                                speak("Sorry, I didn't catch your name.")

                            name_asked = True  # Name has been asked

                        else:

                            with sr.Microphone() as source:
                                print("Jarvis Active...")
                                r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                                audio = r.listen(source)
                                command = r.recognize_google(audio)

                                # process command
                                processCommand(command)

                    except sr.WaitTimeoutError:
                        print("Listening timed out while waiting for phrase to start")
                    except sr.UnknownValueError:
                        print(f"I could not understand the command. Please speak again {' '.join(uname)}")
                    except sr.RequestError as e:
                        print("My Internet Connection got interrupted. Please wait a second and try again...".format(e))

            else:
                active = False

        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
        except sr.UnknownValueError:
            print("I could not understand audio")
        except sr.RequestError as e:
            print("My Internet Connection got interrupted. Please wait a second and try again...".format(e))
