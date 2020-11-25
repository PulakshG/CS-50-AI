import nltk
import sys
import os
import string
import math 

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
    corp={}
    #labels=[]

    for f in os.listdir(directory):
        dPath=(os.path.join(directory,f))
        corp[f]=open(dPath, "r").read() 
    #print("a")
    return corp
    #raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document=document.lower()
    tknz=nltk.word_tokenize(document)
    tnkzPunct=[i for i in tknz if i not in string.punctuation]
    tknzStpw=[i for i in tnkzPunct if i not in nltk.corpus.stopwords.words("english")]
    return [i for i in tknzStpw if i.islower()]
    #raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    df={}
    for document in documents:
        #print(document)
        encounteredWords=set()
        for word in documents[document]:
            #print(word)
            if word not in encounteredWords:
                encounteredWords.add(word)
                if word in df:
                    df[word]+=1
                else:
                    df[word]=1
    idf={}
    nTotalDocuments=len(documents)
    for word in df:
        idf[word]= math.log(nTotalDocuments/df[word]) 
    #print('a',idf)
    return idf
    #raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf=[]
    for document in files:
        tfidfSum=0
        for word in query:
            tf=files[document].count(word)
            #print(tf)
            #print(idfs[word])
            if word in idfs:
                tfidfSum+=tf*idfs[word]
        tfidf.append([document,tfidfSum])
    tfidf.sort(reverse=True, key=(lambda e:e[1])) 
    return [i[0] for i in tfidf[:n]]
    #raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    df=[]
    for sentence in sentences:
        #print(sentence)
        dfSum=0
        for sentenceWord in sentences[sentence]:
            if sentenceWord in query:
                dfSum+=idfs[sentenceWord]
        density=float(len(list(set(sentences[sentence]).intersection(query)))/len(sentences[sentence]))
        df.append([sentence,dfSum,density])
    #print(df)
    df.sort(reverse=True, key=(lambda e:(e[1],e[2]))) 
    #print(df)
    return [i[0] for i in df[:n]]
    #raise NotImplementedError


if __name__ == "__main__":
    main()
