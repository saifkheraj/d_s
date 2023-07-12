from textblob import TextBlob
import wikipedia


def search_wikipedia(name):
    return wikipedia.search(name)


def summarize_wikipedia(name):
    return wikipedia.summary(name)


def get_text_blob(text):
    blob = TextBlob(text)
    return blob


def get_phrases(name):
    text = summarize_wikipedia(name)
    blob = get_text_blob(text)
    phrases = blob.noun_phrases
    return phrases


# golden_state_warriors_text=wikipedia.summary("Golden State Warriors")
# print(get_phrases("Microsoft"))
# print(golden_state_warriors_text)
