from cmath import inf
import nltk
import sys
import os
import math
import string
# nltk.download('stopwords')

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """

    file_names = {}

    for name in os.listdir(directory):
        file_address = os.path.join(directory, name)
        with open(file_address,  encoding="utf-8") as file:
            file_names[name] = file.read()
    return file_names

    # raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = []
    lower_case = document.lower()
    tokenized = nltk.tokenize.word_tokenize(lower_case)

    # Remove punctuations and english stopwords
    for word in tokenized:
        if(word not in string.punctuation and word not in nltk.corpus.stopwords.words("english")):
            words.append(word)
    return words
    # raise NotImplementedError

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    idfs = {}

    # Find Unique words
    # unique_words = set(sum(documents.values(), []))
    unique_words = set()
    for text in documents.values():
        for word in text:
            if word not in unique_words:
                unique_words.add(word)

    # Frequency set for unique words
    for word in unique_words:
        count = 0
        for d in documents.values():
            if(word in d):
                count = count+1
        if count != 0:
            idfs[word] = math.log(len(documents)/count)
    return idfs
    # raise NotImplementedError

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    scores = {}
    for filename, text in files.items():
        score = 0
        for word in query:
            if word in text:
                score = score + text.count(word)*idfs[word]
        if score != 0:
            scores[filename] = score

    sorted_list = [filename for filename, text in sorted(scores.items(), key = lambda x: x[1], reverse = True)][:n]
    return sorted_list
    # raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = {}
    for sentence, words in sentences.items():
        score = 0
        for q in query:
            if q in words:
                score = score + idfs[q]
        
        if score != 0:
            num_in_q = sum([words.count(q) for x in q])
            density = num_in_q/len(words)
            scores[sentence] = (score, density)
    
    sorted_list = [a for a, v in sorted(scores.items(), key = lambda x: (x[1][0], x[1][1]), reverse = True)][:n]
    return sorted_list   
    # raise NotImplementedError

if __name__ == "__main__":
    main()
