import speech_recognition as sr
from gtts import gTTS
import pygame
import openai
import os

import CONFIG

openai.api_key = CONFIG.OPENAI_KEY

recognizer = sr.Recognizer()


def listen():
    with sr.Microphone() as source:
        print("Speak...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
        except:
            print("Not recognized")
            text = "Say something"
        print(f"You said: {text}")
        return text


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.5,
        n=1,
        stop=None,
    ).choices[0].text

    print(response)

    audiofile = "response.mp3"

    tts = gTTS(response, lang='en')
    tts.save(audiofile)

    pygame.mixer.init()
    pygame.mixer.music.load(audiofile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

    os.remove(audiofile)


print("Hi! I'm a voice AI assistant. Speak to me.")

while True:
    text = listen()
    generate_response(text)
