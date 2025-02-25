### Project Description: Multilingual Phrase Flashcard App

#### Overview
The Multilingual Phrase Flashcard App is a desktop application designed to help users learn and practice phrases in multiple languages. This interactive tool uses flashcards and text-to-speech capabilities to enhance the learning experience. The app supports several languages and categories, making it a versatile resource for language learners of all levels.

#### Features
- **Multiple Languages:** Supports French, German, Spanish, and Mexican Spanish.
- **Text-to-Speech:** Pronounces phrases using appropriate voices for each language.
- **User Progress:** Customizable flashcard decks that adapt to user progress.
- **Interactive Flashcards:** Users can flip flashcards to see translations and hear pronunciations.
- **Category Selection:** Users can choose from general, travel, restaurant, dating, and work categories.
- **Learning Direction:** Option to practice translating to English or from English.
- **Language Learning Tips:** Provides useful tips for effective language learning.

#### Usage
1. **Select Language:** Choose the language you want to practice from the dropdown menu.
2. **Select Category:** Choose a category of phrases to focus on.
3. **Change Direction:** Toggle between translating phrases to English or from English.
4. **Flip Flashcards:** Click the "Right" or "Wrong" buttons to proceed through the flashcards.
5. **Listen and Learn:** Hear the correct pronunciation using the text-to-speech feature.

#### Interface
- **Flashcard Display:** Shows the phrase in the selected language or English.
- **Control Buttons:** Includes buttons for flipping cards, changing languages, and categories.
- **Tips Button:** Access language learning tips.

  #### System Requirements
    **Python 3.7+
    **Windows OS (for text-to-speech functionality)
    **Required Python libraries: tkinter, pandas, win32com.client

### GitHub Repository Instructions

#### Repository Overview
This repository contains the source code and data files for the Multilingual Phrase Flashcard App. The project is implemented in Python using Tkinter for the GUI and pandas for data handling.

#### Files and Directories
- **main.py:** The main script to run the application.
- **data/:** Directory containing CSV files for different languages and categories.
- **images/:** Directory containing image files used in the application.
- **requirements.txt:** Expanded requirements list the dependencies required to run the application.

#### Voice Setup
  **The app uses Windows SAPI voices for text-to-speech functionality. To set up voices properly:
  **Go to Windows Settings > Time & Language > Speech
  **Under "Manage voices", install the voices for the languages you want to use
  **The app will automatically detect and use the appropriate voices based on their names:

  **English: Microsoft Zira
  **German: Microsoft Hedda
  **French: Microsoft Hortense
  **Mexican Spanish: Microsoft Sabina
  **Spanish (Spain): Microsoft Helena

If you have different voice names, you may need to modify the setup_voices() function in the code.


CSV Files
The app uses CSV files to store phrases. Each language and category combination should have its own CSV file named as follows:
#### Setup Instructions
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/parkerhill/flash-app-multilingual-phrases.git
   cd flash-app-multilingual-phrases
   ```

2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```sh
   python main.py
   ```

#### CSV Files
- The data directory contains CSV files named in the format `<language>_<category>_phrases.csv`.
- These files contain phrases in the specified language and their English translations.
- Example:
  ```csv
  English,French
  Hello,Bonjour
  Thank you,Merci
  ```

#### Troubleshooting
- **Voice Configuration:** Ensure that the text-to-speech voices are correctly configured on your system.
- **Data Files:** Verify that the CSV files are correctly formatted and located in the `data` directory.

Following these instructions, you can easily set up and run the Multilingual Phrase Flashcard App. Enjoy practicing and enhancing your language skills!
