from matplotlib import pyplot as plt
import requests
from collections import defaultdict, Counter
import string
import re


# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    punctuation = string.punctuation.replace("'", "")
    return text.translate(str.maketrans("", "", punctuation))


def remove_prepositions_and_articles(text):
    pattern = r"\b(?:a|an|the|aboard|about|above|across|after|against|along|amid|among|anti|around|as|at|before|behind|below|beneath|beside|besides|between|beyond|but|by|concerning|considering|despite|down|during|except|excepting|excluding|following|for|from|in|inside|into|like|minus|near|of|off|on|onto|opposite|outside|over|past|per|plus|regarding|round|save|since|than|through|to|toward|towards|under|underneath|unlike|until|up|upon|versus|via|with|within|without)\b"
    cleaned_text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return cleaned_text


def remove_auxiliary_verbs_and_prepositions(text):
    pattern = r"\b(be|am|is|are|was|that|than|no|all|both|each|few|more|most|other|some|such|no|nor|or|not|one|only|own|same|so|than|too|very|s|t|can|will|just|don|should|now|and|were|being|been|have|has|had|do|does|did|doing|will|would|shall|should|may|might|can|could|of|to|in|on|at|by|for|with|about|from|into|through|over|under|above|below|after|before|during|since|until)\b"
    filtered_text = re.sub(pattern, "", text)
    return filtered_text


def remove_pronouns(text):
    pattern = r"\b(?:I|me|my|mine|myself|you|your|yours|yourself|yourselves|he|him|his|himself|she|her|hers|herself|it|its|itself|they|them|their|theirs|themselves|we|us|our|ours|ourselves)\b"
    cleaned_text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return cleaned_text.strip()


def map_function(text):
    words = text.split()
    return [(word, 1) for word in words]


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced


# Виконання MapReduce
def map_reduce(text):
    # Крок 1: Обробка тексту
    processed_punctuation = remove_punctuation(text)
    processed_prepositions = remove_prepositions_and_articles(processed_punctuation)
    processed_auxiliary_verbs = remove_auxiliary_verbs_and_prepositions(
        processed_prepositions
    )
    processed_pronouns = remove_pronouns(processed_auxiliary_verbs)
    # Крок 2: Мапінг
    mapped_values = map_function(processed_pronouns)
    # Крок 3: Shuffle
    shuffled_values = shuffle_function(mapped_values)
    # Крок 4: Редукція
    reduced_values = reduce_function(shuffled_values)
    return reduced_values


def visualize(result):
    top_10 = Counter(result).most_common(10)
    labels, values = zip(*top_10)
    plt.figure(figsize=(10, 5))
    plt.barh(labels, values, color="b", align="center", alpha=0.5, edgecolor="black")
    plt.xlabel("Кількість")
    plt.ylabel("Слово")
    plt.title("10 найпопулярніших слів")
    plt.show()


if __name__ == "__main__":

    # Завантаження тексту з сайту Gutenberg
    URL = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = requests.get(URL).text

    # Виконання MapReduce на вхідному тексті
    result = map_reduce(text)

    # Візуалізація результату
    visualize(result)
