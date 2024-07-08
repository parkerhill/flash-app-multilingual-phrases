import random
import tkinter as tk
from tkinter import messagebox, scrolledtext
import pandas as pd
import win32com.client
import threading
import os

# ---------------------------- CONSTANTS ------------------------------- #
# Color scheme for the application
BACKGROUND_COLOR = "#0076ad"
ALT_BACKGROUND_COLOR = "#80cef3"
PRIMARY_BG = "#121212"
SECONDARY_BG = "#1E1E1E"
ACCENT_COLOR = "#FFD700"
WHT_TEXT_COLOR = "#FFFFFF"
BLK_TEXT_COLOR = "#000000"
WARNING_COLOR = "#FF4500"

# Font settings for different elements
TITLE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 30, "bold")
LABEL_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 10, "bold")

# List of available languages
LANGUAGES = ["French", "German", "Spanish", "Mexican Spanish"]

# List of phrase categories
CATEGORIES = ["general", "travel", "restaurant", "dating", "work"]


# ------------------------- LOAD PHRASES --------------------------- #
def load_phrases(language, direction, category):
    """
    Load phrases from a CSV file based on language, direction, and category.
    If the 'to_learn' file doesn't exist, it creates one from the original phrases file.
    """
    filename = f"data/{language.lower().replace(' ', '_')}_{category}_{direction}_phrases_to_learn.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.read_csv(f"data/{language.lower().replace(' ', '_')}_{category}_phrases.csv")
        df.to_csv(filename, index=False)
    return df


# Global variables
current_language = "French"
current_direction = "to_english"
current_category = "general"
df = load_phrases(current_language, current_direction, current_category)
flip_timer = None
speaker = win32com.client.Dispatch("SAPI.SpVoice")


def setup_voices():
    """
    Set up voice configurations for text-to-speech functionality.
    Maps specific voice names to languages.
    """
    voices = speaker.GetVoices()
    language_voices = {lang: None for lang in LANGUAGES + ["English"]}
    for voice in voices:
        name = voice.GetAttribute("Name").lower()
        if "zira" in name:
            language_voices["English"] = voice
        elif "hedda" in name:
            language_voices["German"] = voice
        elif "hortense" in name:
            language_voices["French"] = voice
        elif "sabina" in name:
            language_voices["Mexican Spanish"] = voice
        elif "helena" in name:
            language_voices["Spanish"] = voice

    print("Configured voices:")
    for lang, voice in language_voices.items():
        if voice:
            print(f"{lang}: {voice.GetAttribute('Name')}")
        else:
            print(f"{lang}: No voice found")

    return language_voices


language_voices = setup_voices()


# ------------------------- TEXT-TO-SPEECH FUNCTIONS --------------------------- #
def speak_text(text, lang):
    """
    Speak the given text in the specified language using text-to-speech.
    """
    try:
        print(f"Attempting to speak '{text}' in {lang}")
        if lang in language_voices and language_voices[lang]:
            voice_name = language_voices[lang].GetAttribute('Name')
            print(f"Setting voice to {voice_name}")
            speaker.Voice = language_voices[lang]
        else:
            print(f"No voice found for {lang}, using default voice")
        speaker.Speak(text)
    except Exception as e:
        print(f"Error speaking text: {e}")


def speak_in_background(text, lang):
    """
    Speak text in a background thread to avoid freezing the GUI.
    """

    def delayed_speak():
        window.after(100, lambda: speak_text(text, lang))

    threading.Thread(target=delayed_speak).start()


# ------------------------- FLASHCARD FUNCTIONS --------------------------- #
def flip_card():
    """
    Display a new flashcard with a phrase in the current language.
    """
    global flip_timer, current_phrase
    if flip_timer:
        window.after_cancel(flip_timer)

    if not df.empty:
        current_phrase = df.sample().iloc[0]
        if current_direction == "to_english":
            foreign_phrase = current_phrase[current_language]
            english_phrase = current_phrase['English']
        else:
            foreign_phrase = current_phrase['English']
            english_phrase = current_phrase[current_language]

        canvas.itemconfig(card_image, image=card_front_img)
        word_label.config(text=foreign_phrase, bg=ALT_BACKGROUND_COLOR, fg=WHT_TEXT_COLOR)
        title_label.config(text=current_language if current_direction == "to_english" else "English",
                           bg=ALT_BACKGROUND_COLOR, fg=WHT_TEXT_COLOR)

        speak_in_background(foreign_phrase, current_language if current_direction == "to_english" else "English")

        flip_timer = window.after(5000, flip_to_translation, english_phrase)
    else:
        word_label.config(text="No more phrases!", bg=ALT_BACKGROUND_COLOR, fg=WHT_TEXT_COLOR)
        title_label.config(text="Congratulations!", bg=ALT_BACKGROUND_COLOR, fg=WHT_TEXT_COLOR)


def flip_to_translation(phrase):
    """
    Flip the flashcard to show the translation.
    """
    canvas.itemconfig(card_image, image=card_back_img)
    word_label.config(text=phrase, bg=WHT_TEXT_COLOR, fg=BACKGROUND_COLOR)
    title_label.config(text="English" if current_direction == "to_english" else current_language, bg=WHT_TEXT_COLOR,
                       fg=BACKGROUND_COLOR)
    speak_in_background(phrase, "English" if current_direction == "to_english" else current_language)


def flip_card_right():
    """
    Handle the user knowing the phrase by removing it from the deck.
    """
    global df
    if not df.empty and 'current_phrase' in globals():
        print(f"Removing phrase: {current_phrase[current_language]} - {current_phrase['English']}")
        df = df[df[current_language if current_direction == "to_english" else 'English'] != current_phrase[
            current_language if current_direction == "to_english" else 'English']]
        df.to_csv(
            f'data/{current_language.lower().replace(" ", "_")}_{current_category}_{current_direction}_phrases_to_learn.csv',
            index=False)
        print(f"Phrases remaining: {len(df)}")
    flip_card()


def flip_card_wrong():
    """
    Handle the user not knowing the phrase by showing a new one.
    """
    flip_card()


def change_language():
    """
    Change the current language and reload phrases.
    """
    global current_language, df
    current_language = language_var.get()
    df = load_phrases(current_language, current_direction, current_category)
    update_language_display()
    flip_card()


def change_direction():
    """
    Toggle between learning to English and from English.
    """
    global current_direction, df
    current_direction = "from_english" if current_direction == "to_english" else "to_english"
    df = load_phrases(current_language, current_direction, current_category)
    update_language_display()
    flip_card()


def change_category():
    """
    Change the current phrase category and reload phrases.
    """
    global current_category, df
    current_category = category_var.get()
    df = load_phrases(current_language, current_direction, current_category)
    update_language_display()
    flip_card()


def update_language_display():
    """
    Update the display to show current language, direction, and category.
    """
    direction_text = "to English" if current_direction == "to_english" else "from English"
    language_label.config(text=f"Current: {current_language} {direction_text} - {current_category}")


def show_language_learning_tips():
    """
    Display a messagebox with language learning tips.
    """
    tips = """
    Language Learning Tips:
    1. Focus on phrases rather than individual words for more natural language use.
    2. Practice speaking from day one, even if you make mistakes.
    3. Immerse yourself in the language through music, movies, and podcasts.
    4. Use spaced repetition techniques for memorization.
    5. Set realistic goals and track your progress.
    6. Find a language exchange partner or join language learning communities.
    7. Learn phrases related to your interests and daily activities.
    8. Don't be afraid to make mistakes - they're part of the learning process.
    9. Try to think in your target language.
    10. Review regularly and use the language whenever possible.

    What to Learn:
    - Common greetings and social phrases
    - Phrases for asking for help or clarification
    - Expressions for ordering food and shopping
    - Directions and transportation-related phrases
    - Basic questions and answers for conversations
    - Phrases for describing yourself and others
    - Common idioms and colloquial expressions
    - Phrases for expressing opinions and emotions
    - Emergency and health-related phrases
    - Cultural-specific expressions and etiquette
    """
    messagebox.showinfo("Language Learning Tips", tips)


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Multilingual Phrase Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = tk.Canvas(window, height=528, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3, rowspan=3, padx=50, pady=50)

# Load images for the flashcards
card_back_img = tk.PhotoImage(file=r"images\card_front_new_blue2.png")
card_front_img = tk.PhotoImage(file=r"images\card_front_new_blue3.png")
wrong_image = tk.PhotoImage(file="images/wrong_new_blue.png")
right_image = tk.PhotoImage(file="images/right_new_blue.png")

card_image = canvas.create_image(400, 264, image=card_front_img)

# Create labels for the flashcard
title_label = tk.Label(window, text="Title", font=TITLE_FONT, bg=ALT_BACKGROUND_COLOR, fg=BLK_TEXT_COLOR)
canvas.create_window(400, 150, window=title_label)

word_label = tk.Label(window, text="Phrase", font=WORD_FONT, bg=ALT_BACKGROUND_COLOR, fg=BLK_TEXT_COLOR, wraplength=700)
canvas.create_window(400, 263, window=word_label)

# Create buttons for user interaction
wrong_button = tk.Button(window, image=wrong_image, command=flip_card_wrong, highlightthickness=0)
wrong_button.grid(row=3, column=0, padx=5, pady=5)

right_button = tk.Button(window, image=right_image, command=flip_card_right, highlightthickness=0)
right_button.grid(row=3, column=2, padx=5, pady=5)

# Create dropdown menus and buttons for language, direction, and category selection
language_var = tk.StringVar(value=current_language)
language_menu = tk.OptionMenu(window, language_var, *LANGUAGES, command=lambda _: change_language())
language_menu.grid(row=4, column=0, padx=5, pady=5)

language_label = tk.Label(window, text=f"Current: {current_language} to English - {current_category}",
                          bg=BACKGROUND_COLOR,
                          fg=WHT_TEXT_COLOR)
language_label.grid(row=4, column=1, padx=5, pady=5)

direction_button = tk.Button(window, text="Change Direction", command=change_direction)
direction_button.grid(row=4, column=2, padx=5, pady=5)

category_var = tk.StringVar(value=current_category)
category_menu = tk.OptionMenu(window, category_var, *CATEGORIES, command=lambda _: change_category())
category_menu.grid(row=5, column=0, padx=5, pady=5)

tips_button = tk.Button(window, text="Language Learning Tips", command=show_language_learning_tips)
tips_button.grid(row=5, column=1, padx=5, pady=5)

# Check if voices are set up correctly
if not language_voices:
    print("Warning: No language voices were set up. Text-to-speech may not work correctly.")


def print_available_voices():
    """
    Print all available voices for debugging purposes.
    """
    voices = speaker.GetVoices()
    for voice in voices:
        print(f"Available voice: {voice.GetAttribute('Name')}")


# Call this function at the start of your program to see available voices
print_available_voices()

# Start the flashcard app
flip_card()

# Run the Tkinter event loop
window.mainloop()
