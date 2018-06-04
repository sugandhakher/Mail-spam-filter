import os
import sys
import string
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords


def get_counts(path):
    s_count = 0
    total = 0
    global doc_id
    for file in os.listdir(path):
        doc_id += 1
        if file.startswith("spmsg"):
            label = True
        else:
            label = False
        if label:
            s_count += 1
        total += 1
        file_path = os.path.join(path, file)
        contents = fetch_contents(file_path)
        contents = pre_process_contents(contents)
        if sys.argv[1] == "bow":
            process_contents(contents, label)
        elif sys.argv[1] == "tfidf":
            process_contents1(contents, label)
        else:
            print "Improper argument!"
            sys.exit(2)
    populate_weights(s_count, total - s_count)
    return s_count, total - s_count


def fetch_contents(file_path):
    with open(file_path, 'r') as label_file:
        contents = label_file.read().replace("\n", '')
        label_file.close()
        return contents


def pre_process_contents(contents):
    for c in string.punctuation:
        contents = contents.replace(c, " ")
        contents = ''.join([i if ord(i) < 123 else '' for i in contents])
    return contents


def process_contents(contents, label):
    global positive_total
    global negative_total

    words = contents.split(" ")
    lemmatizer = WordNetLemmatizer()
    for word in words:
        if word not in stop_list:
            word = lemmatizer.lemmatize(word.lower())
            word = lemmatizer.lemmatize(word.lower(), pos='v')
            if label:
                train_positive[word] = train_positive.get(word, 0) + 1
                positive_total += 1
            else:
                train_negative[word] = train_negative.get(word, 0) + 1
                negative_total += 1


def process_contents1(contents, label):
    temp = {}
    words = contents.split(" ")
    lemmatizer = WordNetLemmatizer()
    for word in words:
        if word not in stop_list:
            word = lemmatizer.lemmatize(word.lower())
            word = lemmatizer.lemmatize(word.lower(), pos='v')
            temp[word] = temp.get(word, 0) + 1
    create_index(temp, label)


def create_index(temp, label):
    for key in temp:
        key = key.encode("ascii", "replace")
        if label:
            if key in positive_index:
                positive_index[key].update({doc_id: temp[key]})
            else:
                positive_index[key] = {doc_id: temp[key]}
        else:
            if key in negative_index:
                negative_index[key].update({doc_id: temp[key]})
            else:
                negative_index[key] = {doc_id: temp[key]}


def populate_weights(s_count, h_count):
    global positive_total
    global negative_total

    for i in positive_index:
        total_frequency = 0
        value = positive_index[i]
        for j in value:
            total_frequency += value[j]
        weight = (total_frequency * s_count) / float(len(value))
        train_positive[i] = weight
        positive_total += weight
    for i in negative_index:
        total_frequency = 0
        value = negative_index[i]
        for j in value:
            total_frequency += value[j]
        weight = (total_frequency * h_count) / float(len(value))
        train_negative[i] = weight
        negative_total += weight

print "Training data now..."
path = os.getcwd() + os.path.sep + 'resources' + os.path.sep + 'bareTraining'
stop_list = stopwords.words('english')
train_positive = {}
train_negative = {}
positive_index = {}
negative_index = {}
positive_total = 0
negative_total = 0
doc_id = 0

spam_count, ham_count = get_counts(path)
p_spam = spam_count / float(spam_count + ham_count)
p_ham = ham_count / float(spam_count + ham_count)
print "Data trained..."
