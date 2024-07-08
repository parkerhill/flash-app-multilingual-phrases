import random
import tkinter as tk
import pandas as pd
import win32com.client
import threading
import os

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#0076ad"
ALT_BACKGROUND_COLOR = "#80cef3"
PRIMARY_BG = "#121212"
SECONDARY_BG = "#1E1E1E"
ACCENT_COLOR = "#FFD700"
WHT_TEXT_COLOR = "#FFFFFF"
BLK_TEXT_COLOR = "#000000"
WARNING_COLOR = "#FF4500"

TITLE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
LABEL_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 10, "bold")

# ------------------------- LOAD WORD PAIRS --------------------------- #
if os.path.exists("data/words_to_learn.csv"):
    df = pd.read_csv("data/words_to_learn.csv")
else:
    df = pd.read_csv("data/500_french_english_pairs.csv")

# Remove duplicates and reset index
df = df.drop_duplicates().reset_index(drop=True)
df.to_csv('data/words_to_learn.csv', index=False)

print(f"Initial word count: {len(df)}")  # Debug print

# Global variables
flip_timer = None
speaker = win32com.client.Dispatch("SAPI.SpVoice")


def setup_voices():
    voices = speaker.GetVoices()
    french_voice = None
    english_voice = None
    for voice in voices:
        if "french" in voice.GetAttribute("Name").lower():
            french_voice = voice
        elif "english" in voice.GetAttribute("Name").lower():
            english_voice = voice
    return french_voice, english_voice


french_voice, english_voice = setup_voices()


# ------------------------- TEXT-TO-SPEECH FUNCTIONS --------------------------- #
def speak_text(text, lang='en'):
    """Speak the given text using the text-to-speech engine in the specified language."""
    try:
        if lang == 'fr' and french_voice:
            speaker.Voice = french_voice
        elif lang == 'en' and english_voice:
            speaker.Voice = english_voice
        speaker.Speak(text)
    except Exception as e:
        print(f"Error speaking text: {e}")


def speak_in_background(text, lang='en'):
    """Speak text in the background with a slight delay to avoid conflicts with Tkinter."""

    def delayed_speak():
        window.after(100, lambda: speak_text(text, lang))

    threading.Thread(target=delayed_speak).start()


# ------------------------- FLASHCARD FUNCTIONS --------------------------- #
def flip_card():
    global flip_timer, current_word
    if flip_timer:
        window.after_cancel(flip_timer)

    if not df.empty:
        current_word = df.sample().iloc[0]
        french_word = current_word['French']
        english_word = current_word['English']

        canvas.itemconfig(card_image, image=card_front_img)
        word_label.config(text=french_word, bg=ALT_BACKGROUND_COLOR, fg=WHT_TEXT_COLOR)
        title_label.config(text="French", bg=ALT_BACKGROUND_COLOR, fg=WHT_TEXT_COLOR)

        speak_in_background(french_word, 'fr')

        flip_timer = window.after(3000, flip_to_english, english_word)
    else:
        word_label.config(text="No more words!", bg=ALT_BACKGROUND_COLOR, fg=WHT_TEXT_COLOR)
        title_label.config(text="Congratulations!", bg=ALT_BACKGROUND_COLOR, fg=WHT_TEXT_COLOR)


def flip_card_right():
    global df, current_word
    if not df.empty and 'current_word' in globals():
        print(f"Removing word: {current_word['French']} - {current_word['English']}")  # Debug print
        df = df[df['French'] != current_word['French']]
        df.to_csv('data/words_to_learn.csv', index=False)
        print(f"Words remaining: {len(df)}")  # Debug print
    flip_card()


def flip_card_wrong():
    flip_card()


def flip_to_english(english_word):
    """Display the English translation of the current word."""
    # Update UI for English word
    canvas.itemconfig(card_image, image=card_back_img)
    word_label.config(text=english_word, bg=WHT_TEXT_COLOR, fg=BACKGROUND_COLOR)
    title_label.config(text="English", bg=WHT_TEXT_COLOR, fg=BACKGROUND_COLOR)

    # Speak the English word
    speak_in_background(english_word, 'en')


# ---------------------------- UI SETUP ------------------------------- #
# Main window setup
window = tk.Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Canvas setup
canvas = tk.Canvas(window, height=528, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3, rowspan=3, padx=50, pady=50)

# Load images
card_back_img = tk.PhotoImage(file=r"images\card_front_new_blue2.png")
card_front_img = tk.PhotoImage(file=r"images\card_front_new_blue3.png")
wrong_image = tk.PhotoImage(file="images/wrong_new_blue.png")
right_image = tk.PhotoImage(file="images/right_new_blue.png")

# Create card image on canvas
card_image = canvas.create_image(400, 264, image=card_front_img)

# Create and place labels
title_label = tk.Label(window, text="Title", font=TITLE_FONT, bg=ALT_BACKGROUND_COLOR, fg=BLK_TEXT_COLOR)
canvas.create_window(400, 150, window=title_label)

word_label = tk.Label(window, text="Word", font=WORD_FONT, bg=ALT_BACKGROUND_COLOR, fg=BLK_TEXT_COLOR)
canvas.create_window(400, 263, window=word_label)

# Create and place buttons
wrong_button = tk.Button(window, image=wrong_image, command=flip_card_wrong, highlightthickness=0)
wrong_button.grid(row=3, column=0, padx=5, pady=5)

right_button = tk.Button(window, image=right_image, command=flip_card_right, highlightthickness=0)
right_button.grid(row=3, column=2, padx=5, pady=5)

# Start the app with a random word
flip_card()

# Start the Tkinter event loop
window.mainloop()

# Test speech after closing the window
speak_text("Test speech in English", 'en')
speak_text("Test de la parole en français", 'fr')
