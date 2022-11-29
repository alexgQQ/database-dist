from random import choice, randint

from faker import Faker

fake = Faker()


class TextGenerator:
    """
    Return random text of defined formats. Subclass this and add more methods
    prefixed with 'name_' to add more options.
    """

    def __init__(self) -> None:
        self.text_funcs = tuple(filter(lambda x: x.startswith("name_"), dir(self)))

    def __call__(self, *args, **kwds) -> str:
        text_func = getattr(self, choice(self.text_funcs))
        return text_func()

    @staticmethod
    def name_random_text() -> str:
        """Random and somewhat gibberish statement"""
        return fake.text(max_nb_chars=randint(10, 35)).replace(".", "")


class ArtistNameGenerator(TextGenerator):
    @staticmethod
    def name_thes() -> str:
        """Random name in the form of 'The Thing Things'"""
        nouns = map(lambda x: x.capitalize(), fake.words(2, "noun"))
        name = "The {} {}".format(*nouns)
        if not name.endswith("s"):
            name += "s"
        return name

    @staticmethod
    def name_single_noun() -> str:
        """Random single capitalized noun"""
        return fake.word("noun").capitalize()

    @staticmethod
    def name_person() -> str:
        """Random full name"""
        return f"{fake.first_name()} {fake.last_name()}"

    @staticmethod
    def name_person_prefix() -> str:
        """Random first name with a prefix like 'Dr. Mike'"""
        return f"{fake.prefix()} {fake.first_name()}"

    @staticmethod
    def name_name_and_the() -> str:
        """Random name in the form of 'John and the Shingles'"""
        noun = fake.word("noun").capitalize()
        noun = noun if noun.endswith("s") else noun + "s"
        name = fake.first_name()
        return f"{name} and the {noun}"

    @staticmethod
    def name_adj_nouns() -> str:
        """Random name as a described noun like 'Angry Beavers'"""
        verb = fake.word("adjective").capitalize()
        noun = fake.word("noun").capitalize()
        noun = noun if noun.endswith("s") else noun + "s"
        return f"{verb} {noun}"


class LabelNameGenerator(TextGenerator):
    @staticmethod
    def name_company() -> str:
        """Random name in company format like 'Wagner LLC Records'"""
        secondary = ("Records", "Sounds", "Music", "Recording")
        return f"{fake.company()} {choice(secondary)}"

    @staticmethod
    def name_verb_records() -> str:
        """Random name in the form of 'Welcoming Records'"""
        verb = fake.word("verb").capitalize()
        verb = verb + "ing" if not verb.endswith("e") else verb[:-1] + "ing"
        secondary = ("Records", "Sounds", "Music", "Recording")
        return f"{verb} {choice(secondary)}"

    @staticmethod
    def name_noun_records() -> str:
        """Random name in the form of 'House Sounds'"""
        secondary = ("Records", "Sounds", "Music", "Recording")
        noun = fake.word("noun").capitalize()
        return f"{noun} {choice(secondary)}"


class AlbumNameGenerator(TextGenerator):
    @staticmethod
    def name_adj_nouns() -> str:
        """Random name as a described noun like 'Angry Beavers'"""
        verb = fake.word("adjective").capitalize()
        noun = fake.word("noun").capitalize()
        noun = noun if noun.endswith("s") else noun + "s"
        return f"{verb} {noun}"

    @staticmethod
    def name_verbing() -> str:
        """Random name as a verb ending in ing"""
        verb = fake.word("verb").capitalize()
        verb = verb + "ing" if not verb.endswith("e") else verb[:-1] + "ing"
        return verb

    @staticmethod
    def name_single_noun() -> str:
        """Random single capitalized noun"""
        return fake.word("noun").capitalize()

    @staticmethod
    def name_things_in_city() -> str:
        """Random name in the form of 'Dog in Tokyo'"""
        return f"{fake.word('noun').capitalize()} in {fake.city()}"

    @staticmethod
    def name_city_verbing() -> str:
        """Random name in the form of 'Denver Walking'"""
        city = fake.city()
        verb = fake.word("verb").capitalize()
        verb = verb + "ing" if not verb.endswith("e") else verb[:-1] + "ing"
        return f"{city} {verb}"


class SongNameGenerator(AlbumNameGenerator):
    pass
