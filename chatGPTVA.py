import speech_recognition as sr
import os
from gtts import gTTS
from dotenv import load_dotenv
from openai import OpenAI

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_KEY)

# Load environment variables from .env file
load_dotenv()

# Ensure you have the correct environment variable set for OpenAI API key

if not OPENAI_KEY:
    raise ValueError("OpenAI API key not set in environment variables.")


def SpeakText(command):
    tts = gTTS(text=command, lang='en')
    tts.save("response.mp3")
    os.system("afplay response.mp3")

r = sr.Recognizer()

def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                print("Listening for ambient noise...")
                r.adjust_for_ambient_noise(source2, duration=0.8)
                print("Listening for speech...")
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                print("Recognized text: " + MyText)
                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError as e:
            print("Unknown error occurred")
            return ""

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(model=model,
    messages=messages,
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.5)
    message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": message})
    return message

messages = [{"role": "user", "content": "You are the virtual assitant Jarvis from IronMan please adress me as Mr.Pena"}]

while True:
    text = record_text()
    if text:
        messages.append({"role": "user", "content": text})
        response = send_to_chatGPT(messages)
        SpeakText(response)
        print(response)
