import gensim
import random

# NB! в pythonanywhere sklearn старой версии, поэтому там используется метод index2entity вместо index_to_key

   
# ф-я импортирует файл {шаблон слова : список подходящих слов}, удаляет невозможные шаблоны, возвращает словарь
def read_patt_word1():
    import dict_rythm_patt_words
    res = dict_rythm_patt_words.dct
    del(res[""])
    del(res["1010"])
    del(res["0"])
    return res


# ф-я импортирует созданный файл и возвращает словарь {слово с ударением : слово без ударения}
def read_vocabulary1():
    import dct_word_stressed
    return dct_word_stressed.dct


# ф-я принимает слово с ударением и возвращает нули и единицы (строкой), которые отображают ритмический шаблон слова
def stress_pattern(stressed):
    vowels_and_stress = "аеёиоуыэюя́"
    li_pattern = [1 if letter == "́" else 0 for letter in stressed if letter in vowels_and_stress]
    res_li = li_pattern[1:]
    return "".join([str(symbol) for symbol in res_li])


# ф-я создает список ритмических шаблонов слов, которые вместе образуют строку с нужным ритмическим шаблоном
def create_line_of_patterns(dct_pattern_word, line_pattern, li_res_pattern):
    if len(line_pattern) > 0:
        pattern = random.choice(list(dct_pattern_word.keys()))
        if line_pattern[:len(pattern)] == pattern and (len(line_pattern[len(pattern):]) > 1 or len(line_pattern[len(pattern):]) == 0):
            li_res_pattern.append(pattern)
            new_pattern = line_pattern[len(pattern):]
            create_line_of_patterns(dct_pattern_word, new_pattern, li_res_pattern)
        else:
            create_line_of_patterns(dct_pattern_word, line_pattern, li_res_pattern)
    return li_res_pattern


# ф-я принимает список слов строки, словарь, шаблон четвертой строки (она должна рифмоваться)
# возвращает список строк
def create_rhyme(li_line_ready, dct_pattern_word, pattern_four):
    li_words = dct_pattern_word[pattern_four]
    last_letters = li_line_ready[-1][-2:]
    while True:
        random_word = random.choice(li_words)
        if last_letters == random_word[-2:]:
            return [random_word]


# ф-я подставляет слова в шаблон, возвращает список слов одной строки
def put_words(first_word, pattern, dct_patt_words, vocab, model, stop_list=[]):
    li_res = []
    previous_word = first_word
    for word_pattern in pattern:
        for candidate, _ in model.most_similar(previous_word, topn=1000):
            if candidate in vocab.keys() and stress_pattern(vocab[candidate]) == word_pattern and candidate not in li_res and candidate not in stop_list:
                li_res.append(candidate)
                previous_word = candidate
                break
        else:
            li_res.append("*")
    return li_res

# ф-я принимает первое слово стихотворения, возвращает список строк готового стихотворения
def create_poem_fin(first_word):
    low_word = first_word.lower()
    if not first_word:
        return ["Введите первое слово стихотворения!"]
    if low_word not in dct_words.keys() or low_word not in model_1.index_to_key:
        flag = True
        while flag:
            candidate = random.choice(model_1.index_to_key)
            if candidate in dct_words.keys() and line_one.startswith(stress_pattern(dct_words[candidate])):
                low_word = candidate
                flag = False
        return [f'В словаре нет такого слова. Попробуйте слово \"{candidate}\" или придумайте другое!']
         
    f_w_patt = stress_pattern(dct_words[low_word])
    if not line_one.startswith(f_w_patt):
        flag = True
        while flag:
            candidate = random.choice(model_1.index_to_key)
            if candidate in dct_words.keys() and line_one.startswith(stress_pattern(dct_words[candidate])):
                low_word = candidate
                flag = False
        return [f'Слово не подходит под ритм. Ударение должно падать на второй слог для соблюдения ритмики. Попробуйте слово \"{candidate}\" или придумайте другое!']

    line_pattern_cut = line_one[len(f_w_patt):]
    
    line_pattern1 = create_line_of_patterns(dct_patt_words, line_pattern_cut, [])
    line_pattern2 = create_line_of_patterns(dct_patt_words, line_two, [])
    line_pattern3 = create_line_of_patterns(dct_patt_words, line_one, [])
    
    word = low_word

    li_line_one = [word, *put_words(word, line_pattern1, dct_patt_words, dct_words, model_1)]
    li_line_two = put_words(li_line_one[-1], line_pattern2, dct_patt_words, dct_words, model_1, li_line_one)
    li_line_three = put_words(li_line_two[-1], line_pattern3, dct_patt_words, dct_words, model_1, li_line_one + li_line_two)
    line4 = create_rhyme(li_line_two, dct_patt_words, line_four)
    return [" ".join(line) for line in [li_line_one, li_line_two, li_line_three, line4]]


path = "C:/Users/сергей/OneDrive/Рабочий стол/poems_site/model_sem.bin"
model_1 = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True) 

dct_words = read_vocabulary1()
dct_patt_words = read_patt_word1()

line_one = "010101010" 
line_two = "01010101" 
line_four = "01" 


#print(create_poem_fin("весна"))


