import json

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class LocalizationManager(metaclass=Singleton):
    def __init__(self, default_language="en"):
        self.default_language = default_language
        self.current_language = default_language
        self.translations = {}

    def load_translations(self, language, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            translations = json.load(file)
            self.translations[language] = translations

    def set_language(self, language):
        if language in self.translations:
            self.current_language = language
        else:
            print(f"Translation for {language} not found. Using default language {self.default_language}.")
            self.current_language = self.default_language

    def translate(self, key):
        if self.current_language in self.translations:
            if key in self.translations[self.current_language]:
                return self.translations[self.current_language][key]
            else:
                print(f"Translation not found for key '{key}' in language '{self.current_language}'")
        else:
            print(f"Translation not found for language '{self.current_language}'")
        return key  # Return the key itself if translation not found