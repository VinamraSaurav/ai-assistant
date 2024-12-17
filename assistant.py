import os
import re
import logging
import webbrowser
import smtplib
import datetime
import traceback
import speech_recognition as sr
import pyttsx3
import wikipedia
import pyautogui
import google.generativeai as genai
from dotenv import load_dotenv
from pytube import YouTube
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# Load environment variables
load_dotenv()

class ComprehensiveAIAssistant:
    def __init__(self):
        self._setup_logging()
        self._setup_speech_systems()
        self._configure_services()

    def _setup_logging(self):
        """Set up logging configuration."""
        log_level = getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper(), logging.INFO)
        log_file = os.getenv('LOG_FILE', 'assistant.log')

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _setup_speech_systems(self):
        """Initialize speech recognition and synthesis."""
        try:
            self.recognizer = sr.Recognizer()
            self.engine = pyttsx3.init()
            
            # Configure voice
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
            self.engine.setProperty('rate', 150)
            
            # Adjust recognizer sensitivity
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            self.logger.error(f"Speech system setup error: {e}")
            self.speak("Error setting up speech systems. Some features may be limited.")

    def _configure_services(self):
        """Configure all external services."""
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')

        wikipedia.set_lang(os.getenv('WIKIPEDIA_LANGUAGE', 'en'))

        try:
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            self.logger.error(f"Gemini AI configuration error: {e}")
            self.gemini_model = None

    def speak(self, text):
        """Convert text to speech."""
        try:
            self.logger.info(f"Speaking: {text}")
            print(f"Assistant: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.logger.error(f"Speech synthesis error: {e}")
            print(f"Speech Error: {text}")

    def listen(self, max_attempts=3):
        """Capture user voice input with multiple retry attempts."""
        for attempt in range(max_attempts):
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    self.speak("Listening...")
                    
                    # Increase timeout and phrase time limit
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                    
                    text = self.recognizer.recognize_google(audio).lower()
                    self.logger.info(f"User said: {text}")
                    return text
            
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand your speech. Please try again.")
                self.logger.warning(f"Speech recognition could not understand audio (Attempt {attempt + 1})")
            
            except sr.RequestError as e:
                self.speak("Speech recognition service is unavailable.")
                self.logger.error(f"Could not request results from speech recognition service: {e}")
                return ""
            
            except sr.WaitTimeoutError:
                self.speak("Listening timed out. No speech detected.")
                self.logger.warning(f"Listening timed out (Attempt {attempt + 1})")
        
        self.speak("Multiple listening attempts failed. Please check your microphone.")
        return ""

    def gemini_query(self, query):
        if not self.gemini_model:
            self.speak("Gemini AI is not configured.")
            return "I'm sorry, the AI service is currently unavailable."

        try:
            response = self.gemini_model.generate_content(query)
            
            # Preprocess the response text
            processed_text = response.text
            
            # Remove asterisks
            processed_text = processed_text.replace('*', '')
            
            # Remove extra whitespaces
            processed_text = ' '.join(processed_text.split())
            
            return processed_text.strip()
        except Exception as e:
            self.logger.error(f"Gemini AI error: {e}")
            return f"I encountered an error processing your request: {e}"


    def youtube_search(self, query):
        """Search for a YouTube video and open the first result."""
        try:
            self.speak(f"Searching YouTube for {query}.")
            search_url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(search_url)
        except Exception as e:
            self.logger.error(f"YouTube search error: {e}")
            self.speak("I encountered an error while searching YouTube.")

    def web_search(self, query):
        """Perform a Google search and open the results page."""
        try:
            self.speak(f"Searching the web for {query}.")
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(search_url)
        except Exception as e:
            self.logger.error(f"Web search error: {e}")
            self.speak("I encountered an error while performing the web search.")

    def run(self):
        """Main assistant loop with fallback input method."""
        self.speak("Hello! I'm your AI assistant. How can I help you today?")

        while True:
            command = self.listen()
            if not command:
                self.speak("Voice input failed. Please type your command.")
                command = input("You: ").lower()

            if command in ['exit', 'bye', 'quit']:
                self.speak("Goodbye! Have a great day.")
                break

            try:
                if "play" in command or "youtube" in command:
                    self.youtube_search(command.replace("play", "").replace("youtube", "").strip())
                elif "search the web" in command or "perform web search" in command:
                    self.web_search(command.replace("search the web", "").replace("perform web search", "").strip())
                else:
                    response = self.gemini_query(command)
                    self.speak(response)
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                self.speak("I encountered an unexpected error. Please try again.")

if __name__ == "__main__":
    assistant = ComprehensiveAIAssistant()
    try:
        assistant.run()
    except Exception as e:
        logging.error(f"Critical error: {traceback.format_exc()}")
