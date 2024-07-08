import pyperclip
import random
import tkinter as tk
from tkinter import messagebox
import json
import csv

# ---------------------------- CONSTANTS ------------------------------- #
# Color palette
BACKGROUND_COLOR = "#0076ad"
PRIMARY_BG = "#121212"  # Very Dark Gray, almost Black
SECONDARY_BG = "#1E1E1E"  # Slightly Lighter Dark Gray
ACCENT_COLOR = "#FFD700"  # Gold
WHT_TEXT_COLOR = "#FFFFFF"  # White
BLK_TEXT_COLOR = "#000000"
WARNING_COLOR = "#FF4500"  # Orange-Red

# Fonts
TITLE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
LABEL_FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 10, "bold")


# ------------------------- GET RANDOM WORD PAIR --------------------------- #
# Function to get a random word pair
def get_random_word_pair():
    # Path to your CSV file
    csv_file_path = "data/french_words.csv"

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)

        # Skip the header row
        next(csv_reader)

        # Convert the CSV reader to a list
        word_list = list(csv_reader)

        # Check if the list is not empty
        if word_list:
            # Choose a random row
            random_pair = random.choice(word_list)
            french_word, english_word = random_pair
            print(f"Random French word: {french_word}")
            print(f"English translation: {english_word}")
            word_label.config(text=french_word)
            title_label.config(text=english_word)
            return random_pair
        else:
            return None


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# # Dictionary to store the translations
translations = {}

# Path to your CSV file
csv_file_path = "data/french_words.csv"

# Read the CSV file
with open(csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    # Skip the header row
    next(csv_reader)

    # Read each row and add to the dictionary
    for row in csv_reader:
        if len(row) == 2:
            french, english = row
            translations[french] = english

# Print the dictionary to verify
print(translations)

# Example usage
print(translations.get("partie"))  # Output: part
print(translations.get("histoire"))  # Output: history

# Create and place the canvas