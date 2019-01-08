import numpy as np
import lda
import lda.datasets
from sklearn.feature_extraction.text import CountVectorizer
import json

# # document-term matrix
# X = lda.datasets.load_reuters()
# print("type(X): {}".format(type(X)))
# print("shape: {}\n".format(X.shape))
# print(X[:5, :5])
#
# # the vocab
# vocab = lda.datasets.load_reuters_vocab()
# print("type(vocab): {}".format(type(vocab)))
# print("len(vocab): {}\n".format(len(vocab)))
# print(vocab[:5])
#
# # titles for each story
# titles = lda.datasets.load_reuters_titles()
# print("type(titles): {}".format(type(titles)))
# print("len(titles): {}\n".format(len(titles)))
# print(titles[:5])

# f = open("data1.txt", encoding='utf-8')  #设置以utf-8解码模式读取文件，encoding参数必须设置，否则默认以gbk模式读取文件，当文件中包含中文时，会报错
# data = json.load(f)


def readin():
    corpus = []
    ids = []
    i = 0
    for line in open("~/paper_sun_shen.txt", 'r', encoding='utf-8').readlines():
        # if i < 100:
            jline = json.loads(line)
            corpus.append(jline['abstract'])
            ids.append(jline['paperid'])
            i = i + 1

    return corpus, ids


def paper_lda(corpus, n_topics, n_iter):
    vectorizer = CountVectorizer(stop_words='english')
    print(vectorizer)
    X = vectorizer.fit_transform(corpus)
    analyze = vectorizer.build_analyzer()
    vocab = list(tuple(vectorizer.vocabulary_))
    vocab.sort()

    print("type(X): {}".format(type(X)))
    print("shape: {}\n".format(X.shape))
    print(X[:5, :5])
    print("type(vocab): {}".format(type(vocab)))
    print("len(vocab): {}\n".format(len(vocab)))
    print(vocab[:5])

    model = lda.LDA(n_topics=n_topics, n_iter=n_iter, random_state=1)
    model.fit(X)          # model.fit_transform(X) is also available

    topic_word = model.topic_word_
    n = 10
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
        print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))

    doc_topic = model.doc_topic_
    for n in range(10):
        topic_most_pr = doc_topic[n].argmax()
        print("doc: {} topic: {}".format(n, topic_most_pr))

    return vocab, topic_word, doc_topic


def writeout(vocab, topic_word, doc_topic):
    file = open('vocab.txt', 'w', encoding='utf-8')
    file.write(str(vocab))
    file.close()
    np.savetxt("topic_word.txt", topic_word)
    np.savetxt("doc_topic.txt", doc_topic)

