#need to import stuff from Total English Assistant to get vocab words
#create separate list of questions to randomly choose from too.
import pyglet
import temporarydatasolution as tds

showing_black_box = False

class Problem(pyglet.text.Label):

    vocab_black_box_img = pyglet.resource.image("black_box.png")
    vocab_black_box = pyglet.sprite.Sprite(vocab_black_box_img, x = 345, y = 264)
    question_center_x = vocab_black_box_img.width // 2 + vocab_black_box.x
    question_center_y = vocab_black_box_img.height // 2 + vocab_black_box.y
    english_vocab_guide = pyglet.text.Label(text = "Translate to Japanese", font_name = "Comic Sans MS", anchor_x = "center",  x = question_center_x, y = question_center_y + 60, font_size = 12)
    english_sentence_guide = pyglet.text.Label(text = "Translate to Japanese", font_name = "Comic Sans MS", anchor_x = "center",  x = question_center_x, y = question_center_y + 60, font_size = 12)
    present_verb_guide = pyglet.text.Label(text = "Translate to Japanese", font_name = "Comic Sans MS", anchor_x = "center",  x = question_center_x, y = question_center_y + 60, font_size = 12)
    japanese_vocab_guide = pyglet.text.Label(text = "Translate to English", font_name = "Comic Sans MS", anchor_x = "center",  x = question_center_x, y = question_center_y + 60, font_size = 12)
    pronunciation_guide = pyglet.text.Label(text = "Speak", font_name = "Comic Sans MS", anchor_x = "center",  x = question_center_x, y = question_center_y + 60, font_size = 12)

    def __init__(self, x = 345, y = 300, text = "blank",  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q_x = Problem.question_center_x
        self.q_y = Problem.question_center_y
        self.question = pyglet.text.Label(text = "blank", font_name = "Comic Sans MS", x = self.q_x, y = self.q_y, font_size = 24)
        self.question.anchor_x = "center"
        self.question.anchor_y = "center"
        self.data = tds.Data()
#        self.present_verb_guide = pyglet.text.Label(text = "present verb guide", font_name = "Comic Sans MS", x = 300, y = 300, font_size = 18)
#        self.past_verb_guide = pyglet.text.Label(text = "past verb guide", font_name = "Comic Sans MS", x = 300, y = 300, font_size = 18)
#        self.japanese_translation_guide = pyglet.text.Label(text = "japanese translation guide", font_name = "Comic Sans MS", x = 300, y = 300, font_size = 18)
#        self.target_sentence_guide= pyglet.text.Label(text = "target sentence guide", font_name = "Comic Sans MS", x = 300, y = 300, font_size = 18)
#        self.image_guide = pyglet.text.Label(text = "image guide", font_name = "Comic Sans MS", x = 300, y = 300, font_size = 18)
    
    def random_english_word(self):
        """Chooses a random English vocabulary word. Returns None."""
        #Student should translate the English word into Japanese
        random_word = self.data.english_word()
        basic_format = random_word + " "
        self.question.text = self.data.english_word() 

    def random_japanese_word(self):
        """Chooses a random Japanese vocabulary word. Returns None."""
        choice = self.data.english_word()
        self.question.text = self.data.japanese_word() 
    
    def random_image(self):
        """Chooses a random word and loads the associated image. Returns None."""
        self.question.text = "image word" 
        #need to change the size of the image to fit within the Vocab box dimensions
        #not completed in temporarydatasolution.py

    def random_present_verb(self):
        """Chooses random type of present-tense verb. Returns None."""
        self.question.text = self.data.random_verb() 

    def random_verb_form(self):
        """Chooses a random verb form from a random verb. Returns None."""
        self.question.text = self.data.random_verb_form()

    def random_past_verb(self):
        """Chooses a random verb's past form. Returns None."""
        self.question.text = self.data.random_past_verb() 
    
#    def continuous_verb(self):
#        """Chooses a random verb's continuous form. Returns None."""
#        self.question.text = self.data.random_continuous_verb() 

    def random_target_sentence(self):
        """Chooses a random target sentence. Returns None."""
        self.question.text = self.data.random_target_sentence() 

    def random_pronunciation(self):
        """Chooses a random word that is difficult to pronuounce. Returns None."""
        self.question.text = self.data.random_pronunciation() 
