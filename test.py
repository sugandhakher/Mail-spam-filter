import os
import string
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from train import p_spam, p_ham, train_positive, train_negative, positive_total, negative_total


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


def conditional(word, label):
    if label:
        return (train_positive.get(word, 1))/float(positive_total + len(train_positive) + len(train_negative))
    else:
        return (train_negative.get(word, 1))/float(negative_total + len(train_positive) + len(train_negative))


def conditional_email(contents, spam):
    result = 1.0
    lemmatizer = WordNetLemmatizer()
    words = contents.split(" ")
    for word in words:
        if word not in stop_list:
            word = lemmatizer.lemmatize(word.lower())
            word = lemmatizer.lemmatize(word.lower(), pos='v')
            result *= conditional(word, spam)
    return result


def classify(contents):
    global spam_prediction
    global ham_prediction
    isSpam = p_spam * conditional_email(contents, True)
    isHam = p_ham * conditional_email(contents, False)
    if isSpam > isHam:
        return True
    else:
        return False

print "Testing predictions now..."
path = os.getcwd() + os.path.sep + 'resources' + os.path.sep + 'bareTesting'
stop_list = stopwords.words('english')
spam_prediction = 0
ham_prediction = 0
true_positive = 0
false_positive = 0
false_negative = 0
true_negative = 0

for file in os.listdir(path):
    file_path = os.path.join(path, file)
    contents = fetch_contents(file_path)
    contents = pre_process_contents(contents)
    if classify(contents):
        if file.startswith("spmsg"):
            true_positive += 1
        else:
            false_positive += 1
        spam_prediction += 1
    else:
        if file.startswith("spmsg"):
            false_negative += 1
        else:
            true_negative += 1
        ham_prediction += 1

print "Tests complete..."
