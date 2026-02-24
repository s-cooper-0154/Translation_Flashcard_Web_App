import os
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
load_dotenv ()
import spacy as sp
from googletrans import Translator
trans = Translator ()

app = Flask (__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-very-unsafe')

@app.route ("/")
def index ():
  return render_template ("index.html")

@app.route ("/backend", methods = ["POST"])
def make_flashcards ():
  #Extracting input information
  language = request.form.get ("input_text_language")
  content = request.form.get ("input_text")

  #Importing language model based on input
  if language == "zhongwen":
     import_language = "zh_core_web_sm"
  else:
    import_language = language[0 : 2] + "_core_news_sm"

  nlp = sp.load (import_language)

  #Converting all characters to lowercase (if applicable)
  lower_content = str.lower (content)

  #Importing Matcher tool and establishing key variables
  from spacy.matcher import Matcher
  matcher = Matcher (nlp.vocab)  

  info = nlp (lower_content)
  vocab_list = []

  #Extracting determiners, adjectives, and nouns together
  det_pattern1 = [{"POS" : "DET"}, {"POS" : "NOUN"}]
  det_pattern2 = [{"POS" : "DET"}, {"POS" : "ADJ"}, {"POS" : "NOUN"}]
  det_pattern3 = [{"POS" : "DET"}, {"POS" : "PROPN"}]
  det_pattern4 = [{"POS" : "DET"}, {"POS" : "ADJ"}, {"POS" : "PROPN"}]

  matcher.add ("D_N_Determiner_Pattern", [det_pattern1])
  matcher.add ("D_A_N_Determiner_Pattern", [det_pattern2])
  matcher.add ("D_PN_Determiner_Pattern", [det_pattern3])
  matcher.add ("D_A_PN_Determiner_Pattern", [det_pattern4])

  #Extracting prepositional phrases
  prep_pattern1 = [{"POS" : "ADP"}, {"POS" : "NOUN"}]
  prep_pattern2 = [{"POS" : "ADP"}, {"POS" : "PROPN"}]
  prep_pattern3 = [{"POS" : "ADP"}, {"POS" : "PRON"}]
  prep_pattern4 = [{"POS" : "ADP"}, {"POS" : "ADJ"}, {"POS" : "NOUN"}]
  prep_pattern5 = [{"POS" : "ADP"}, {"POS" : "ADJ"}, {"POS" : "PROPN"}]

  prep_pattern1 = [{"POS" : "ADP"}, {"POS" : "NOUN"}]
  prep_pattern2 = [{"POS" : "ADP"}, {"POS" : "PROPN"}]
  prep_pattern3 = [{"POS" : "ADP"}, {"POS" : "PRON"}]
  prep_pattern4 = [{"POS" : "ADP"}, {"POS" : "ADJ"}, {"POS" : "NOUN"}]
  prep_pattern5 = [{"POS" : "ADP"}, {"POS" : "ADJ"}, {"POS" : "PROPN"}]

  #Finding matches in text
  matches = matcher (info)

  for match_id, start, end in matches:
    vocab_list.append (info[start : end])
    
  #Removing words already added to vocab list from document
  lower_content_copy = lower_content
  for match_id, start, end in matches:
    lower_content_copy = lower_content_copy.replace (info[start : end].text, "")
    
  info_new = nlp (lower_content_copy)

  #Extracting other parts of speech from remaining text
  for token in info_new: 
    if token.pos_ != "NUM" and token.pos_ != "PUNCT" and token.pos_ != "SYM" and token.pos_ != "Space" and token.pos_ != "DET" and token.pos_ != "ADP":
      vocab_list.append (token)

  #Filtering duplicates
  vocab_list_uniq = list (set ([str (item)for item in vocab_list]))

  #Translating and creating dictionaries
  vocab_to_be_translated = str (vocab_list_uniq)

  raw_translation = trans.translate (vocab_to_be_translated, dest = 'en').text
  raw_translation = raw_translation.replace ("'", "")

  list_translation = raw_translation.split (",")
  list_translation = [item.replace ("[", "") for item in list_translation]
  
  definitions = []
  for word in vocab_list_uniq:
    definitions.append ({
      "Word" : word,
      "Translation" : list_translation[vocab_list_uniq.index (word)]
    })

  #Creating flashcards
  front_side = []
  back_side = []

  def flashcards (x):
    for vocab_term in x:
      front_side.append (vocab_term["Word"])
      back_side.append (vocab_term["Translation"])
    
  flashcards (definitions)

  flashcard_deck = []
  for f, b in zip (front_side, back_side):
    flashcard_deck.append ({"Front" : f, "Back" : b})

  session["Cards"] = flashcard_deck

  return redirect(url_for("show_cards"))

@app.route ("/display_cards")
def show_cards ():
  my_cards = session.get ("Cards", [])
  return render_template ("display_cards.html", cards = my_cards)


if __name__ == '__main__':
    app.run(debug=True)