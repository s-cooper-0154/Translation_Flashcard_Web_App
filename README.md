# Translation Flashcard Web App
Flashcard generator for learning foreign languages.
## About
This Flask web app allows the user to input text in a foreign language, which will be analyzed in order to extract not only vocabulary terms, but also grammatical phrases including adjectives, prepositions, and determiner words. These terms and phrases will then be used to create flashcards for the user to study.
### Supported Languages
Currently, this web app supports translation from Greek, Mandarin, Russian, and Spanish into English. 
### More About Grammatical Phrases
This web app uses the NLP spaCy matcher to find set patterns in the uploaded text. These patterns include:

* Determiner and noun 
* Determiner, adjective, and noun 
* Preposition and noun
  
More complex grammatical structures may not be recognized by the matcher.
## How to Use 
1. Clone the repository 
2. Open a virtual environment on your computer.
3. Install the requirements in the "requirements.txt" (**pip install -r requirements.txt**)
4. Run the "Translation_App.py" and open up the local URL returned
## Future Plans
This is an ongoing project, and I intend on bettering the web app in several ways, including:

* Updating the interace to make it more visually appealing
* Adding a save function so a user can have multiple flashcard decks at once
* Identifying a wider variety of grammatical patterns
* Including pertinent information on each flashcard (including tense, case, plurality, gender, etc.)
* Increasing the number of compatible languages
