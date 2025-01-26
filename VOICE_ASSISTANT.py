import speech_recognition as sr
import pyttsx3
import datetime
import requests
import wikipedia
from bs4 import BeautifulSoup

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    print(f"Assistant: {text}")  # Debugging - prints what the assistant will say
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen for a voice command and return it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please say it again.")
        except sr.RequestError:
            speak("Sorry, I can't connect to the speech recognition service.")
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred while processing your command.")
        return None

def search_google(query):
    """Perform a backend search on Google and return a snippet."""
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            snippet = soup.find("div", class_="BNeawe").text
            return snippet
        else:
            return "I couldn't retrieve the information from Google."
    except Exception as e:
        print(f"Google Search Error: {e}")
        return "An error occurred while searching Google."

def search_wikipedia(query):
    """Perform a Wikipedia search and return a summary."""
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your query is ambiguous. Please specify one of the following: {', '.join(e.options[:3])}"
    except wikipedia.exceptions.PageError:
        return "I couldn't find any matching results on Wikipedia."
    except Exception as e:
        print(f"Wikipedia Error: {e}")
        return "An error occurred while searching Wikipedia."

def handle_command(command):
    """Process and respond to the given command."""
    if command is None:
        return

    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif "date" in command:
        today_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today_date}.")
    elif "search google for" in command or "google" in command:
        search_query = command.replace("search google for", "").replace("google", "").strip()
        if search_query:
            speak(f"Searching Google for {search_query}.")
            result = search_google(search_query)
            speak(result)
        else:
            speak("Please specify what you'd like me to search for on Google.")
    elif "search wikipedia for" in command or "wikipedia" in command:
        search_query = command.replace("search wikipedia for", "").replace("wikipedia", "").strip()
        if search_query:
            speak(f"Searching Wikipedia for {search_query}.")
            result = search_wikipedia(search_query)
            speak(result)
        else:
            speak("Please specify what you'd like me to search for on Wikipedia.")
    elif "exit" in command or "quit" in command:
        speak("Goodbye! Have a great day!")
        exit()
    else:
        speak(f"I can't perform the task '{command}' yet, but I'm learning!")

def main():
    """Main function to run the voice assistant."""
    speak("Hello! I am your assistant. How can I help you?")
    while True:
        command = take_command()
        if command:
            handle_command(command)

if __name__ == "__main__":
    main()
