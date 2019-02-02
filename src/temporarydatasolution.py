#stand lib
import json
import random
import string
import sys

#3rd party

#custom
from gamedata.customquestions import * 
from gamedata.pronunciation import *
from gamedata.targetsentences import *
from gamedata.targetsentencesjapanese import *
from gamedata.verbforms import *
from src.constants import *

class Data():
    """Creates instance of chosen dictionary. Returns none."""
    default_dict_path   = "gamedata/totalenglish123.json" 
    default_dict_name   = "totalenglish123"
    default_dict        = "totalenglish123.json"
    default_entry       = {"not found":"not found"}
    
    #eng target sentences
    b1_ets = eng_book_1
    b2_ets = eng_book_2
    b3_ets = eng_book_3
    
    #jap target sentences
    b1_jts = jap_book_1
    b2_jts = jap_book_2
    b2_jts = jap_book_3

    verb_forms          = verb_forms    
    questions           = questions
    pronunciation_words = words
    lowercase           = string.ascii_lowercase

    nouns       = []
    verbs       = []
    pronouns    = []
    adjectives  = []   
    e_ts        = []
    j_ts        = []

    def __init__(self):
        """Prepares word list of the dictionary, returns None."""
        self.dictionary = self.load_dictionary()
        self.words      = self.get_words()
        self.size       = len(self.words)
        self.initialize_nouns()
        self.initialize_verbs()
        self.initialize_pronouns()
        self.initialize_adjectives()
        self.initialize_target_sentences()

    #LOAD DATA
    def load_dictionary(self):
        """Loads dictionary. Returns Dictionary.""" 
        with open(self.default_dict_path) as file_object:
#            self.dictionary = json.load(file_object)
            return json.load(file_object)
        
    def add_words_from_grade(self, grade):
        """Adds words based on grade level. Returns None."""
        words = self.words
        dict_ = self.dictionary
        for word in dict_.keys():
            if grade == int(dict_[word]["grade"]):
                words.append(word)

    def get_words(self):
        """Gets words. Returns List."""
        words = []
        dict_ = self.dictionary
        for grade in GRADES:
            words += self.grade_words(grade, dict_)

        #filter words in the max grade based on page range 
        from_ = PAGE_RANGE[0]
        until = PAGE_RANGE[1] 
        filteredwords = []
        for word in words:
            page = int(self.dictionary[word]["page"])
            if self.within(page, from_, until):
                filteredwords.append(word)
        return filteredwords
    
    def within(self, page, f, u):
        """Checks page is within range. Returns Boolean."""
        return page >= f and page <= u

    def grade_words(self, grade, dict_):
        """Gets words in a grade. Returns List."""
        words = []
        for word in self.dictionary.keys():
            if grade == int(self.dictionary[word]["grade"]):
                words.append(word)
        return words

    def filter_words_by_punctuation(self):
        """Filters out words with punctutation. Returns List."""
        list_ = []
        for word in self.words:
            if "'" in word:
                list_.append(word)
        return list_

    def initialize_nouns(self):
        """Filters nouns to a list. Returns None."""
        for word in self.dictionary.keys():
            if self.dictionary[word]["part of speech"] == "noun":
                self.nouns.append(word)

    def initialize_verbs(self):
        """Loads verbs normal forms. Returns None."""
        for key in self.verb_forms.keys():
            self.verbs.append(key)

    def initialize_pronouns(self):
        """Filters pronouns to a list. Returns None."""
        for word in self.dictionary.keys():
            if self.dictionary[word]["part of speech"]=="pronoun":
                self.pronouns.append(word)

    def initialize_adjectives(self):
        """Filters adjectives to a list. Returns None."""
        for word in self.dictionary.keys():
            if self.dictionary[word]["part of speech"]=="adjective":
                self.adjectives.append(word)

    def initialize_target_sentences(self):
        """Loads English target sentences. Returns None."""
        for sentence in self.b1_ets:
            self.e_ts.append(sentence)
        for sentence in self.b2_ets:
            self.e_ts.append(sentence)
        for sentence in self.b3_ets:
            self.e_ts.append(sentence)

    def initialize_japanese_target_sentences(self):
        """Loads Japanese target sentences. Returns None."""
        for sentence in self.b1_jts:
            self.j_ts.append(sentence)
        for sentence in self.b2_jts:
            self.j_ts.append(sentence)
        for sentence in self.b2_jts:
            self.j_ts.append(sentence)

    #WORDS
    def japanese_word(self, word):
        """Gets the Japanese definition. Returns String."""
        return self.dictionary[word]["japanese"]

    def english_word(self):
        """Gets a random English word. Returns String."""
        return random.choice(self.words)

    def random_verb_form(self):
        """Gets a random verb in a random form. Returns String."""
        choice = random.choice(self.verbs)
        verb_forms = self.verb_forms[choice].keys()
        form_choice = random.choice(verb_forms)
        if type(self.verb_forms[choice][form_choice]) == list:
            return self.verb_forms[choice][form_choice][0]
        return self.verb_forms[choice][form_choice]        

    def random_verb(self):
        """Gets a random, present-tense verb. Returns String."""
        return random.choice(self.verbs)

    def random_past_verb(self):
        """Gets a random, past-tense verb. Returns String."""
        choice = random.choice(self.verbs)
        if type(self.verb_forms[choice]["past"]) == list:
            return self.verb_forms[choice]["past"][0]
        return self.verb_forms[choice]["past"]        

    def random_pronunciation(self):
        """Gets difficult to pronounce word. Returns String."""
        return random.choice(self.pronunciation_words)

    #SENTENCES
    def random_target_sentence(self):
        """Gets random target sentence. Returns String."""
        return random.choice(self.e_ts)

    def random_target_sentence_japanese(self):
        """Gets random japanese target sentence. Returns String."""
        return random.choice(self.j_ts)

    def random_question(self):
        """Gets random question. Returns String."""
        return random.choice(self.questions)
