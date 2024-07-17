import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import threading
import tkinter as tk
from tkinter import ttk
import pyperclip
import ctypes
import os

class SpeechTranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Translation App")

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Increase font size by 7 times
        label_font = ("TkDefaultFont", 10)
        translated_label_font = ("TkDefaultFont", 5 * 10)

        style = ttk.Style()
        style.configure("TButton", font=label_font)
        style.configure("TLabel", font=translated_label_font)

        self.translated_label = ttk.Label(root, text="", style="TLabel")
        self.translated_label.pack(pady=10)

        self.copy_button = ttk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard, style="TButton")
        self.copy_button.pack(pady=10)

        self.save_button = ttk.Button(root, text="Save as MP3", command=self.save_to_mp3, style="TButton")
        self.save_button.pack(pady=10)

        self.start_button = ttk.Button(root, text="Start Recording", command=self.toggle_translation, style="TButton")
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop Recording", command=self.stop_recording, state="disabled", style="TButton")
        self.stop_button.pack(pady=10)

        self.translation_enabled = False

        # Initialize pyttsx3
        self.engine = pyttsx3.init()

    def recognize_speech(self):
        with self.microphone as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        try:
            text = self.recognizer.recognize_google(audio, language="ru-RU")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Error making request: {e}")
            return None

    def toggle_translation(self):
        if not self.translation_enabled:
            self.translation_enabled = True
            self.start_button["state"] = "disabled"
            self.stop_button["state"] = "normal"
            self.copy_button["state"] = "normal"
            self.save_button["state"] = "normal"
            threading.Thread(target=self.continuous_translation).start()
        else:
            self.translation_enabled = False

    def continuous_translation(self):
        while self.translation_enabled:
            speech_text = self.recognize_speech()
            if speech_text:
                self.translated_label["text"] = speech_text
                self.speak(speech_text)

        # Set the flag to False after recording is finished
        self.translation_enabled = False
        # Restore buttons to their initial state after stopping recording
        self.start_button["state"] = "normal"
        self.stop_button["state"] = "disabled"
        self.copy_button["state"] = "disabled"
        self.save_button["state"] = "disabled"

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def stop_recording(self):
        self.translation_enabled = False

    def copy_to_clipboard(self):
        translated_text = self.translated_label["text"]
        pyperclip.copy(translated_text)

    def save_to_mp3(self):
        translated_text = self.translated_label["text"]
        if translated_text:
            tts = gTTS(translated_text, lang='ru')
            tts.save("translated_text.mp3")
            print("Translated text saved as MP3 file: translated_text.mp3")
        else:
            print("No text to save as MP3.")

if __name__ == "__main__":
    # Set console colors for Windows
    ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x8 | 0xf)  # Dark gray background, white text

    root = tk.Tk()
    app = SpeechTranslationApp(root)
    root.mainloop()
