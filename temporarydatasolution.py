#std lib
import json
import random
import sys
import string

#custom
from constants import Constants as c

if "./gamedata" not in sys.path:
    sys.path.append("./gamedata")

import verbforms
import targetsentences 
import customquestions          #custom made for this game
import targetsentencesjapanese
import pronunciation            #custom made for this game

class Data():
    """Creates an instance of the chosen dictionary, returns none."""
    default_dict_path = "./gamedata/totalenglish123.json" 
    default_dict_name = "totalenglish123"
    default_dict = "totalenglish123.json"
    default_entry = {"not found":"not found"}
    
    book_1_target_sentences = targetsentences.eng_book_1
    book_2_target_sentences = targetsentences.eng_book_2
    book_3_target_sentences = targetsentences.eng_book_3
    
    book_1_japanese_target_sentences = targetsentencesjapanese.jap_book_1
    book_2_japanese_target_sentences = targetsentencesjapanese.jap_book_2
    book_3_japanese_target_sentences = targetsentencesjapanese.jap_book_3

    verb_forms = verbforms.verb_forms    
    questions = customquestions.questions
    pronunciation_words = pronunciation.words
    lowercase = string.ascii_lowercase

    nouns = []
    verbs = []
    pronouns = []
    adjectives = []   
    target_sentences = []
    japanese_target_sentences = []

    def __init__(self):
        """Prepares word list of the dictionary, returns None."""
        self.dictionary = {}
        self.load_dictionary()
        self.words = []
#        self.sort_words()                   #this also loads words into self.words
        self.load_words()

        #these are filtered in stages as shown
#        self.grade_filtered = []            #words filtered by grade level
#        self.page_range_filtered = []       #words filtered by page_range

        self.size = len(self.words)
        self.initialize_nouns()
        self.initialize_verbs()
        self.initialize_pronouns()
        self.initialize_adjectives()
        self.initialize_target_sentences()
#        print("length of game dictionary = ", self.size)
#        print("length of actual dictionary = ", len(self.dictionary))
    
    def load_dictionary(self):
        """Loads the dictionary from the path set in the instance, returns None."""
        with open(self.default_dict_path) as file_object:
            self.dictionary = json.load(file_object)

    def load_words(self):
        """Loads words into self.words based on grade levels and page ranges. Returns None."""
        for grade in c.GRADES:
            self.add_words_from_grade(grade)
        
    def add_words_from_grade(self, grade):
        """Adds to self.words based on grade level. Returns None."""
        for word in self.dictionary.keys():
            if grade == int(self.dictionary[word]["grade"]):
                self.words.append(word)
#
#    def sort_words(self):
#        """Sorts the 'words' list, returns None."""
#        for key in self.dictionary.keys():
#            self.words.append(key)
#        self.words = sorted(self.words)
#
#    def filter_words_by_grade(self, grade):
#        """Filters the 'words' list by user-specified student grade level. Returns String."""
#        words = []
#        for word in self.words:
#            if grade == int(self.dictionary[word]["grade"]):
#                words.append(word)
##        return len(words)
#        return words

    def filter_words_by_punctuation(self):
        """Filters the 'words' list of words with punctutation, returns List."""
        list_ = []
        for word in self.words:
            if "'" in word:
                list_.append(word)
        return list_

    def initialize_nouns(self):
        """Filters the nouns into an easy to access list, returns None."""
        for word in self.dictionary.keys():
            if self.dictionary[word]["part of speech"] == "noun":
                self.nouns.append(word)

    def initialize_verbs(self):
        """Pre-loads list of verbs' normal forms that appear in the verb form table in the back of the Total English books. Returns None."""
        for key in self.verb_forms.keys():
            self.verbs.append(key)

    def initialize_pronouns(self):
        """Filters the pronouns into an easy to access list, returns None."""
        for word in self.dictionary.keys():
            if self.dictionary[word]["part of speech"] == "pronoun":
                self.pronouns.append(word)

    def initialize_adjectives(self):
        """Filters the adjectives into an easy to access list, returns None."""
        for word in self.dictionary.keys():
            if self.dictionary[word]["part of speech"] == "adjective":
                self.adjectives.append(word)

    def initialize_target_sentences(self):
        """Gets a random target sentence from all 3 grades. Returns String."""
        for sentence in self.book_1_target_sentences:
            self.target_sentences.append(sentence)
        for sentence in self.book_2_target_sentences:
            self.target_sentences.append(sentence)
        for sentence in self.book_3_target_sentences:
            self.target_sentences.append(sentence)

    def initialize_japanese_target_sentences(self):
        """Gets a random target sentence from all 3 grades. Returns String."""
        for sentence in self.book_1_japanese_target_sentences:
            self.japanese_target_sentences.append(sentence)
        for sentence in self.book_2_japanese_target_sentences:
            self.japanese_target_sentences.append(sentence)
        for sentence in self.book_3_japanese_target_sentences:
            self.japanese_target_sentences.append(sentence)
        
    def japanese_word(self, word: str) -> str:
        """Gets the Japanese definition."""
        return self.dictionary[word]["japanese"]

    def english_word(self) -> str:
        """Gets a random English word."""
        return random.choice(self.words)

    def random_verb_form(self) -> str:
        """Gets a random verb in a random form."""
        choice = random.choice(self.verbs)
        verb_forms = self.verb_forms[choice].keys()
        verb_forms = ["normal", "present", "past", "past participle", "gerund"]
        form_choice = random.choice(verb_forms)
        if type(self.verb_forms[choice][form_choice]) == list:
            return self.verb_forms[choice][form_choice][0]
        return self.verb_forms[choice][form_choice]        

    def random_verb(self) -> str:
        """Gets a random, present-tense verb."""
        return random.choice(self.verbs)

    def random_past_verb(self) -> str:
        """Gets a random, past-tense verb."""
        choice = random.choice(self.verbs)
        if type(self.verb_forms[choice]["past"]) == list:
            return self.verb_forms[choice]["past"][0]
        return self.verb_forms[choice]["past"]        

    def random_target_sentence(self):
        """Gets a random target sentence. Returns String."""
        return random.choice(self.target_sentences)

    def random_target_sentence_japanese(self):
        """Gets a random japanese target sentence. Returns String."""
        return random.choice(self.japanese_target_sentences)

    def random_pronunciation(self) -> str:
        """Gets a random word that is difficult to pronounce."""
        return random.choice(self.pronunciation_words)
