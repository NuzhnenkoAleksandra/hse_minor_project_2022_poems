from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import gensim
import logging
import urllib.request

import warnings
warnings.filterwarnings('ignore')

from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()


rus_letters = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя") 


# функция для очистки данного текста, который считывается из файла
def cleaned_text(file):
    with open(file, "r", encoding="utf-8") as f_r: 
        text = f_r.read()
        res_text = []
        sentences = sent_tokenize(text) # одно предложение - одна строка
        for sentence in sentences:
            tokens = word_tokenize(sentence) # делим предложения на словоформы (токены)
            no_punct = [w.lower() for w in tokens if w.isalpha() and set(w) <= rus_letters]
            stops = stopwords.words('russian')
            filtered = [w for w in no_punct if w not in stops] # исключение стоп-слов
            res_sentence = " ".join(filtered)
            res_text.append(res_sentence)
        return res_text       

stops = stopwords.words("russian")

tfidf = TfidfVectorizer(
    analyzer="word", # анализировать по словам или по символам (char)
    stop_words=stops # передаём список стоп-слов для русского из NLTK
)


# подготовка итогового файла
dir_path="C:/Users/сергей/OneDrive/Рабочий стол/poems/books_model"
files = os.listdir(dir_path)
print(files)
with open("C:/Users/сергей/OneDrive/Рабочий стол/poems/main_file_semant.txt", "a", encoding="utf-8") as f_w:
    for name in files: # цикл по всем названиям файлов в папке
        path = dir_path + "/" + name # формирование пути к данному файлу
        res_text = cleaned_text(path) # обработка файла через функцию, приводящую текст к нужному виду
        for line in res_text:
            f_w.write(line + "\n") # запись данных


# обучение модели
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
f = 'C:/Users/сергей/OneDrive/Рабочий стол/poems/main_file_semant.txt'
data = gensim.models.word2vec.LineSentence(f)
semant_model = gensim.models.Word2Vec(data, vector_size=300, window=5, min_count=5, epochs=50)


# сохранение обученной модели
semant_model.wv.save_word2vec_format("C:/Users/сергей/OneDrive/Рабочий стол/poems/model_sem.bin", binary=True)


