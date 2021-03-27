import collections
import math
import os
import string

import nltk
import pymorphy2
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from alphabet_detector import AlphabetDetector
from stop_words import get_stop_words

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

STOP_WORDS = stopwords.words('russian')
STOP_WORDS.extend(stopwords.words('english'))
STOP_WORDS.extend(get_stop_words('ru'))
STOP_WORDS.extend(get_stop_words('en'))
STOP_WORDS.extend(string.punctuation)

AD = AlphabetDetector()
POS_CONSTANTS = ['a', 's', 'r', 'n', 'v']


def get_pos_tag(token):
    tag = nltk.pos_tag([token])[0][1][0].lower()
    if tag in POS_CONSTANTS:
        return tag
    return 'n'


def compute_tf(text):
    tf_text = collections.Counter(text)
    for i in tf_text:
        tf_text[i] = round(tf_text[i] / float(len(text)), 4)
    return tf_text


def compute_idf(word, corpus):
    return round(
        math.log10(len(corpus) / sum([1.0 for i in corpus if word in i])), 4)


def compute_tfidf(corpus):
    documents_list = []
    already_written_idfs = []
    with open(f'/Users/daniilkarpov/Desktop/Github/infoSearch/WebParserCrawler/src/result/idf/idf.txt', 'w', encoding='utf-8') as idf_file:
        idf_file.write("{:<30} {:<30}\n".format('Term', 'IDF'))

        for num, text in enumerate(corpus, start=1):
            tf_idf_dictionary = {}
            computed_tf = compute_tf(text)
            with open(f'/Users/daniilkarpov/Desktop/Github/infoSearch/WebParserCrawler/src/result/tf/{num}-terms-tf.txt', 'w', encoding='utf-8') as file:
                lines = ["{:<30} {:<30}\n".format('Term', 'TF')]
                lines.extend(["{:<30} {:<30}\n".format(k, v) for k, v in
                              computed_tf.items()])
                file.writelines(lines)

            for word in computed_tf:
                computed_idf = compute_idf(word, corpus)

                if word not in already_written_idfs:
                    already_written_idfs.append(word)
                    idf_file.write(
                        "{:<30} {:<30}\n".format(word, computed_idf))

                tf_idf_dictionary[word] = round(
                    computed_tf[word] * computed_idf, 4)

            documents_list.append(tf_idf_dictionary)

            with open(f'/Users/daniilkarpov/Desktop/Github/infoSearch/WebParserCrawler/src/result/tf-idf/{num}-terms-tf-idf.txt', 'w',
                      encoding='utf-8') as tf_idf_file:
                lines = ["{:<30} {:<30}\n".format('Term', 'TF-IDF')]
                lines.extend(["{:<30} {:<30}\n".format(k, v)
                              for k, v in sorted(tf_idf_dictionary.items(),
                                                 key=lambda p: p[1],
                                                 reverse=True)])
                tf_idf_file.writelines(lines)

    return documents_list


def tokenize(text, morph, wordnet_lemmatizer):
    tokens = nltk.word_tokenize(text, language='russian')
    tokens = [t.lower() for t in tokens if t.isalpha()]
    tokens = [t.lower() for t in tokens if t not in STOP_WORDS]
    tokens = [morph.parse(t)[0].normal_form if AD.is_cyrillic(t)
              else wordnet_lemmatizer.lemmatize(t, pos=get_pos_tag(t))
              for t in tokens]
    return tokens


if __name__ == '__main__':
    morph = pymorphy2.MorphAnalyzer()
    wordnet_lemmatizer = WordNetLemmatizer()

    corpus = []
    for name in os.listdir('/Users/daniilkarpov/Desktop/Github/infoSearch/WebParserCrawler/src/result/'):
        file_name, file_extension = os.path.splitext(name)
        if file_extension == '.txt' and file_name != 'index':
            with open('/Users/daniilkarpov/Desktop/Github/infoSearch/WebParserCrawler/src/result/' + name, 'r', encoding='utf-8') as file:
                corpus.append(tokenize(file.read(), morph, wordnet_lemmatizer))

    compute_tfidf(corpus)
