import os
import JarvisAI
import re
import pprint
import random
import pygame # type: ignore
import requests # type: ignore
import tkinter as tk

MUSIC_DIR = "/path/to/music/directory"

assistant = JarvisAI.JarvisAssistant()

def t2s(text: str) -> None:
    """
    Convert text to speech using the JarvisAI library.
    """
    try:
        assistant.text2speech(text)
    except Exception as e:
        print(f"Error: {e}")

def play_music() -> None:
    """
    Play a random song from the music directory.
    """
    try:
        if not os.path.exists(MUSIC_DIR):
            t2s("Music directory not found")
            return
        songs = os.listdir(MUSIC_DIR)
        if not songs:
            t2s("No songs found in music directory")
            return
        song = random.choice(songs)
        pygame.init()
        pygame.mixer.music.load(f"{MUSIC_DIR}/{song}")
        pygame.mixer.music.play()
        t2s(f"Playing {song}")
    except Exception as e:
        t2s("Error playing music")



def tell_joke() -> None:
    """
    Tell a random joke using a joke API.
    """
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke_res = response.json()
        t2s(joke_res['setup'])
        t2s(joke_res['punchline'])
    except Exception as e:
        t2s("Error getting joke")

def get_definition(word: str) -> None:
    """
    Get the definition of a word using the JarvisAI library.
    """
    try:
        if not word:
            t2s("Please enter a word")
            return
        definition = assistant.dictionary(word)
        if not definition:
            t2s("Word not found in dictionary")
            return
        t2s(definition)
    except JarvisAIErrors.WordNotFoundError:
        t2s("Word not found in dictionary")
    except Exception as e:
        t2s(f"Error getting definition: {e}")

def get_weather(city: str) -> None:
    """
    Get the weather for a given city using the JarvisAI library.
    """
    try:
        if not city:
            t2s("Please enter a city name")
            return
        weather_res = assistant.weather(city=city)
        if not weather_res:
            t2s("Weather information not available for this city")
            return
        t2s(weather_res)
    except JarvisAIErrors.CityNotFoundError:
        t2s("City not found")
    except JarvisAIErrors.WeatherAPIError:
        t2s("Error getting weather from API")
    except Exception as e:
        t2s(f"Error getting weather: {e}")


def get_news() -> None:
    """
    Get the news using a news API.
    """
    try:
        response = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY")
        news_res = response.json()
        t2s(f"I have found {len(news_res['articles'])} news. You can read it. Let me tell you first 2 of them")
        t2s(news_res['articles'][0]['title'])
        t2s(news_res['articles'][1]['title'])
    except Exception as e:
        t2s(f"Error getting news: {e}")

def get_weather(city: str) -> None:
    """
    Get the weather for a given city using a weather API.
    """
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY")
        weather_res = response.json()
        t2s(f"Weather in {city}: {weather_res['weather'][0]['description']}")
    except Exception as e:
        t2s(f"Error getting weather: {e}")

import tkinter as tk

class JarvisGUI:
    def __init__(self, master):
        self.master = master
        master.title("Jarvis Assistant")

        # Create frames
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(fill="x")

        self.output_frame = tk.Frame(master)
        self.output_frame.pack(fill="both", expand=True)

        # Create input field
        self.input_field = tk.Entry(self.input_frame, width=50)
        self.input_field.pack(side="left", fill="x", expand=True)

        # Create send button
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_input)
        self.send_button.pack(side="right")

        # Create output text box
        self.output_text = tk.Text(self.output_frame)
        self.output_text.pack(fill="both", expand=True)

    def send_input(self):
        input_text = self.input_field.get()
        self.input_field.delete(0, "end")

        # Process input text
        if re.search('weather|temperature', input_text):
            city = input_text.split(' ')[-1]
            get_weather(city)
            self.output_text.insert("end", f"Weather in {city}:\n")
            self.output_text.insert("end", get_weather(city) + "\n")

        elif re.search('news', input_text):
            get_news()
            self.output_text.insert("end", "News:\n")
            self.output_text.insert("end", get_news() + "\n")

        elif re.search('play music', input_text):
            play_music()
            self.output_text.insert("end", "Playing music...\n")

        elif re.search('joke', input_text):
            tell_joke()
            self.output_text.insert("end", "Joke:\n")
            self.output_text.insert("end", tell_joke() + "\n")

        elif re.search('define', input_text):
            word = input_text.split(' ')[-1]
            get_definition(word)
            self.output_text.insert("end", f"Definition of {word}:\n")
            self.output_text.insert("end", get_definition(word) + "\n")

        elif re.search('exit', input_text):
            self.master.destroy()

        else:
            self.output_text.insert("end", "I didn't understand that. Please try again.\n")

root = tk.Tk()
my_gui = JarvisGUI(root)
root.mainloop()

def main() -> None:
    """
    Main function to handle user input.
    """
    while True:
        try:
            res = assistant.mic_input()
        except Exception as e:
            t2s("Error getting user input")
            continue

        if re.search('weather|temperature', res):
            city = res.split(' ')[-1]
            get_weather(city)

        elif re.search('news', res):
            get_news()

        elif re.search('play music', res):
            play_music()

        elif re.search('joke', res):
            tell_joke()

        elif re.search('define', res):
            word = res.split(' ')[-1]
            get_definition(word)

        elif re.search('exit', res):
            t2s("Goodbye!")
            break

        else:
            t2s("I didn't understand that. Please try again.")

if __name__ == "__main__":
    main()