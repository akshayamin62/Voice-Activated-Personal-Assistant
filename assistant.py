import speech_recognition as sr
import pyttsx3
import keyboard
import subprocess
import webbrowser
import datetime
import sys
import requests
import threading
import os
import time
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)

# Helper: Speak text aloud
def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Helper: Listen for a voice command
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        speak("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return ""

# --- Modular Command Functions ---
def greet_command(command):
    speak("Hello! How can I help you?")

def open_notepad(command):
    speak("Opening Notepad.")
    subprocess.Popen(["notepad.exe"])

def open_calculator(command):
    speak("Opening Calculator.")
    subprocess.Popen(["calc.exe"])

def open_website(command):
    speak("Which website should I open?")
    site = listen()
    if site:
        url = f"https://{site}" if not site.startswith("http") else site
        speak(f"Opening {url}")
        webbrowser.open(url)

def search_web(command):
    speak("What should I search for?")
    query = listen()
    if query:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        speak(f"Searching for {query}")
        webbrowser.open(url)

def tell_time(command):
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

def tell_date(command):
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {today}")

def exit_command(command):
    speak("Goodbye!")
    sys.exit(0)

# --- System Control ---
def system_control(command):
    if "volume up" in command:
        for _ in range(5):
            keyboard.press_and_release('volume up')
        speak("Volume increased.")
    elif "volume down" in command:
        for _ in range(5):
            keyboard.press_and_release('volume down')
        speak("Volume decreased.")
    elif "mute" in command:
        keyboard.press_and_release('volume mute')
        speak("Volume muted.")
    elif "brightness up" in command:
        speak("Brightness up is not natively supported on all Windows devices.")
    elif "brightness down" in command:
        speak("Brightness down is not natively supported on all Windows devices.")
    elif "lock" in command:
        speak("Locking your computer.")
        ctypes = __import__('ctypes')
        ctypes.windll.user32.LockWorkStation()
    elif "shutdown" in command:
        speak("Shutting down your computer.")
        os.system("shutdown /s /t 1")
    elif "restart" in command:
        speak("Restarting your computer.")
        os.system("shutdown /r /t 1")
    else:
        speak("System control command not recognized.")

# --- News (Placeholder) ---
def read_news(command):
    speak("News feature requires an API key. Please add your NewsAPI key to config.py.")

# --- Weather (Placeholder) ---
def read_weather(command):
    speak("Weather feature requires an API key. Please add your OpenWeatherMap key to config.py.")

# --- Reminders and Alarms ---
def reminder_thread(message, seconds):
    time.sleep(seconds)
    speak(f"Reminder: {message}")

def set_reminder(command):
    speak("What should I remind you about?")
    message = listen()
    if not message:
        speak("Reminder cancelled.")
        return
    speak("In how many minutes?")
    try:
        minutes = int(listen())
        seconds = minutes * 60
        threading.Thread(target=reminder_thread, args=(message, seconds), daemon=True).start()
        speak(f"Reminder set for {minutes} minutes from now.")
    except Exception:
        speak("Sorry, I couldn't set the reminder.")

# --- Play Music or Video ---
def play_music(command):
    if "YouTube" in command:
        speak("What should I play on YouTube?")
        query = listen()
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            speak(f"Playing {query} on YouTube.")
            webbrowser.open(url)
    else:
        speak("Please say the full path to the music or video file you want to play.")
        file_path = listen()
        if file_path and os.path.exists(file_path):
            speak(f"Playing {file_path}")
            os.startfile(file_path)
        else:
            speak("File not found or path not recognized.")

# --- Groq LLM Smart Response ---
def groq_smart_response(command):
    speak("Let me think...")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are Jarvis, a helpful AI assistant for Windows."},
            {"role": "user", "content": command}
        ],
        "max_tokens": 256,
        "temperature": 0.7
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        result = response.json()
        answer = result['choices'][0]['message']['content']
        speak(answer)
    except Exception as e:
        speak("Sorry, I couldn't get a smart response.")
        print(e)

# --- Command Routing ---
COMMANDS = [
    (lambda c: any(greet in c for greet in ["hello", "hi", "hey"]), greet_command),
    (lambda c: "notepad" in c, open_notepad),
    (lambda c: "calculator" in c, open_calculator),
    (lambda c: "open" in c and "website" in c, open_website),
    (lambda c: "search" in c, search_web),
    (lambda c: "time" in c, tell_time),
    (lambda c: "date" in c, tell_date),
    (lambda c: any(x in c for x in ["exit", "quit", "stop"]), exit_command),
    (lambda c: any(x in c for x in ["volume", "brightness", "lock", "shutdown", "restart", "mute"]), system_control),
    (lambda c: "news" in c, read_news),
    (lambda c: "weather" in c, read_weather),
    (lambda c: "remind" in c or "alarm" in c, set_reminder),
    (lambda c: "music" in c or "video" in c or "play" in c, play_music),
]

def handle_command(command):
    for matcher, func in COMMANDS:
        if matcher(command):
            func(command)
            return
    # If no command matched, use Groq smart response
    groq_smart_response(command)

# Main loop: Wait for hotkey, then listen and handle command
def main():
    speak("Jarvis is running. Press Ctrl+Shift+J to talk. Say 'help' for a list of features.")
    while True:
        keyboard.wait('ctrl+shift+j')
        command = listen()
        if command == "help":
            speak("You can say: open notepad, open calculator, open website, search, time, date, volume up, volume down, mute, lock, shutdown, restart, remind me, play music, play video, play on youtube, or just ask anything.")
            continue
        if command:
            handle_command(command)

if __name__ == "__main__":
    main() 