from resources.lexicon import lexicon
from langdetect import detect


# Function to identify doc language
def is_urdu_or_english(text):
    lang = detect(text).replace("lang.", "")
    return "en" if lang != "en" and lang != "ur" else lang


# Get formatted root term keyword
def get_root_term(term):
    return lexicon[term]
