from datetime import datetime
import pickle
import os


class RepetitionInfo:

    def __init__(self, success):
        self.success = success
        self.time = datetime.today()


class RepetitionHistory:

    def __init__(self):
        self.history = []
    
    def add_repetition_result(self, success):
        self.history.append(RepetitionInfo(success))


class Word:

    def __init__(self, word):
        self.word = word
        self.last_repeated = datetime.today()
        self.first_entered = datetime.today()
        self.repetition_history = RepetitionHistory()

    def __str__(self):
        return self.first_entered.strftime("%B %d, %Y")


    def repeat(self):

        print(self.word, end=" ")

        while True:

            answer = input("Remember [Y / n]:")

            if answer.lower().startswith("y"):
                self.repetition_history.add_repetition_result(True)
                break
            elif answer.lower().startwith("n"):
                self.repetition_history.add_repetition_result(False)
                break
            else:
                print("Unknown option, use [Y / n]")
    


class Vocabulary():

    def __init__(self, filepath_to_store_info):
        self.filepath_to_store_info = filepath_to_store_info
        self.words = []

    def add_word(self, word):
        self.words.append(Word(word))

    def generate_list_for_repetition(self, length=None):
        lst = sorted(self.words, key=lambda word: word.last_repeated, reverse=True)
        try:
            return lst[:length]
        except IndexError:
            return lst
    
    def store_to_disk(self):
        with open(self.filepath_to_store_info, "wb") as f:
            pickle.dump(self, f)

    @classmethod   
    def load_existing_vocabulary(cls, path):
        with open(path, "rb") as f:
            vocabulary = pickle.load(f)
        return vocabulary

    def show_stats(self):
        print(f"Words in total {len(self.words)}")

        
if __name__ == "__main__":

    path_to_file = os.path.join(os.environ["HOME"], f".{os.environ['USER']}'sWordsToLearn")

    if os.path.exists(path_to_file):
        vocabulary = Vocabulary.load_existing_vocabulary(path_to_file)
    else:
        vocabulary = Vocabulary(path_to_file)

    vocabulary.show_stats()

    print("""Commands:
    repeat {your number} - queries the words that were not repeated the longed and goes into the repeat mode
    show stats - shows stats
    quit - quits the program
    add {your word} - adds a new word to the vocabulary""")

    working = True
    while working:

        command = input("> ")

        if command == "show stats":
            vocabulary.show_stats()

        elif command == "quit":
            working = False

        elif command.startswith("repeat"):
            command_name, param  = command.split(" ")
            if param.isdigit():
                lst = vocabulary.generate_list_for_repetition(int(param))
                for word in lst:
                    word.repeat()

        elif command.startswith("add"):
            command_name, param  = command.split(" ")
            vocabulary.add_word(param)
        else:
            print("unknown command")

    vocabulary.store_to_disk()