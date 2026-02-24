# Translation Flashcard Web App
Flashcard generator for learning foreign languages.
## About
This Flask web app allows the user to input text in a foreign language, which will be analyzed in order to extract not only vocabulary terms, but also grammatical phrases including adjectives, prepositions, and determiner words. These terms and phrases will then be used to create flashcards for the user to study.
### Supported Languages
Currently, the web app supports translation from Greek, Mandarin, Russian, and Spanish into English. 
### More About Grammatical Phrases
This web app uses an NLP (spaCY) matcher to find set patterns in your text. These patterns include:

* Determiner and noun 
* Determiner, adjective, and noun 
* Preposition and noun
  
More complex grammatical structures may not be recognized by the matcher.
## How to Use 
1. Download the app files
2. Open a virtual environment on your computer.
3. Install the requirements in the "requirements.txt" (**pip install -r requirements.txt**)
4. Run the "Translation_App.py" and open up the local URL returned

