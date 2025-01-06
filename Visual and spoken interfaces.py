import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import pywhatkit
import urllib.parse
import psutil  # Library to handle system processes
import pyautogui  # Library to simulate keyboard shortcuts
import datetime
import random
import time  # To add delays if needed

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Speech Recognition Function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            speak_text("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            speak_text("Sorry, my speech service is currently down.")
            return None

# Text-to-Speech Function
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to get the current time
def get_current_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    time_responses = [
        f"The current time is {now}.",
        f"It's {now}. Time flies, doesn't it?",
        f"Right now, it's {now}."
    ]
    return random.choice(time_responses)

# Function to open applications and websites
def open_application(command):
    if "open youtube" in command.lower():
        speak_text("Opening YouTube for you. Enjoy exploring!")
        webbrowser.open("https://www.youtube.com")
    elif "play" in command.lower() and "youtube" in command.lower():
        song = command.lower().replace("play", "").replace("youtube", "").strip()
        if song:
            speak_text(f"Let's listen to {song} on YouTube. Enjoy the music!")
            pywhatkit.playonyt(song)
            time.sleep(5)  # Adding a delay to ensure the song starts playing
        else:
            speak_text("I'd love to play a song, but I need to know which one.")
    elif "github" in command.lower():
        speak_text("Let's head to GitHub. Happy coding!")
        webbrowser.open("https://www.github.com")
    elif "maps" in command.lower():
        location = command.lower().replace("maps", "").strip()
        if location:
            query = urllib.parse.quote(location)
            url = f"https://www.google.com/maps/search/?api=1&query={query}"
            speak_text(f"Finding directions to {location}. Safe travels!")
            webbrowser.open(url)
        else:
            speak_text("Taking you to Google Maps.")
            webbrowser.open("https://maps.google.com")
    elif "matlab" in command.lower():
        speak_text("Opening MATLAB. Ready to crunch some numbers?")
        os.system("matlab")
    else:
        speak_text("I'm not sure how to open that application or website, sorry!")

# Function to bring YouTube window to the front
def focus_youtube():
    for proc in psutil.process_iter():
        if proc.name() in ["chrome.exe", "firefox.exe", "msedge.exe"]:
            for cmdline in proc.cmdline():
                if "youtube" in cmdline:
                    if proc.name() == "chrome.exe":
                        os.system("wmctrl -a 'Google Chrome'")
                    elif proc.name() == "firefox.exe":
                        os.system("wmctrl -a 'Mozilla Firefox'")
                    elif proc.name() == "msedge.exe":
                        os.system("wmctrl -a 'Microsoft Edge'")
                    return True
    return False

# Function to control YouTube playback
def control_youtube(command):
    if focus_youtube():
        if "pause youtube" in command.lower():
            speak_text("Pausing YouTube playback.")
            pyautogui.press("k")  # 'k' is the shortcut key to play/pause on YouTube
        elif "play youtube" in command.lower():
            speak_text("Resuming YouTube playback.")
            pyautogui.press("k")  # 'k' is the shortcut key to play/pause on YouTube
        elif "next youtube" in command.lower():
            speak_text("Skipping to the next video on YouTube.")
            pyautogui.press("shift+n")  # 'Shift+N' is the shortcut key to play the next video on YouTube
    else:
        speak_text("No active YouTube window found.")

# Function to close YouTube browser tabs
def close_youtube():
    for proc in psutil.process_iter():
        if proc.name() in ["chrome.exe", "firefox.exe", "msedge.exe"]:
            if "youtube" in proc.cmdline():
                proc.terminate()
    speak_text("YouTube tabs have been closed.")

# Function to close all browser tabs
def close_browsers():
    for proc in psutil.process_iter():
        if proc.name() in ["chrome.exe", "firefox.exe", "msedge.exe"]:
            proc.terminate()
    speak_text("All browser tabs have been closed.")

# Function to handle the dynamic intro and listening
def dynamic_intro():
    intros = [
        "Hi there! I'm Sam, your voice-controlled assistant. How can I help you today?",
        "Hello! I'm Sam, ready to assist you. What would you like to do?",
        "Greetings! I'm Sam, your AI assistant. How can I assist you today?",
        "Hey there! Sam here, at your service. What can I do for you?",
    ]
    speak_text(random.choice(intros))

def listen_and_respond():
    print("Waiting for wake word...")
    command = recognize_speech()
    if command and "sam" in command.lower():
        print("Wake word detected!")
        dynamic_intro()
        while True:
            print("Listening for your command...")
            command = recognize_speech()
            if command:
                process_command(command)
            time.sleep(1)  # Add a short delay before listening for the next command

def process_command(command):
    greetings = ["hi", "hello", "hey"]
    if any(greeting in command.lower() for greeting in greetings):
        speak_text("Hello! I'm Sam, your assistant. How can I assist you today?")
    elif "how are you" in command.lower():
        responses = [
            "I'm just a bunch of code, but thanks for asking! How about you?",
            "I'm doing well, thank you! How can I assist you today?",
            "I'm here and ready to help! How are you?",
            "Feeling great, thank you! What's on your mind?"
        ]
        speak_text(random.choice(responses))
    elif any(phrase in command.lower() for phrase in ["i am feeling great", "i am good", "i am alright", "i am fine", "never better"]):
        responses = [
            "That's wonderful to hear! What else can I do for you?",
            "Awesome! I'm glad to hear that. How can I assist you?",
            "Great to hear! If there's anything you need, just let me know.",
            "Fantastic! I'm here if you need anything else."
        ]
        speak_text(random.choice(responses))
    elif "time" in command.lower():
        current_time = get_current_time()
        speak_text(current_time)
    elif "thank you" in command.lower():
        thank_responses = [
            "You're welcome! Happy to help.",
            "No problem at all!",
            "Anytime! Glad I could assist."
        ]
        speak_text(random.choice(thank_responses))
    elif "joke" in command.lower():
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't skeletons fight each other? They don't have the guts.",
            "What do you call fake spaghetti? An impasta!",
            "Why was the math book sad? It had too many problems."
        ]
        speak_text(random.choice(jokes))
    elif "exit" in command.lower():
        speak_text("Goodbye! Have a great day!")
        os._exit(0)
    elif "stop youtube" in command.lower():
        close_youtube()
    elif any(playback in command.lower() for playback in ["pause youtube", "play youtube", "next youtube"]):
        control_youtube(command)
    else:
        open_application(command)

if __name__ == "__main__":
    listen_and_respond()
