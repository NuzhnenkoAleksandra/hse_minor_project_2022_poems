import json
import random


# принимает слово с ударением и возвращает слово без ударения
def remove_stress(word):
    return word.replace("́", "")


# принимает словарь и возвращает список форм слова
def json_to_forms(data):
    if "forms" in data.keys():
        return [i["form"] for i in data["forms"]]
    else:
        return []
    

# из начального файла формирует словарь вида {слово с ударением : слово без ударения}
def create_vocabulary():
    with open('C:/Users/сергей/OneDrive/Рабочий стол/kaikki.org-dictionary-Russian.json') as json_file:    
        with open('C:/Users/сергей/OneDrive/Рабочий стол/test1.txt', "w", encoding="utf-8") as f:
            dct_words = {}
            c = 0
            for line in json_file:
                c += 1
                data = json.loads(line)
                li_forms = json_to_forms(data)
                for word in li_forms:
                    word_lower = word.lower()
                    not_stressed = remove_stress(word_lower)
                    if (not_stressed in one_symb_word) or (len(not_stressed) > 1 and set(not_stressed).issubset(cyr_symbols)):
                        dct_words[not_stressed] = word_lower
                if c % 1000 == 0:
                    print(c)
            json.dump(dct_words, f, ensure_ascii=False)
    return dct_words


# принимает слово с ударением и возвращает из нули и единицы (строкой), который отображает ритмический шаблон слова
def stress_pattern(stressed):
    vowels_and_stress = "аеёиоуыэюя́"
    li_pattern = [1 if letter == "́" else 0 for letter in stressed if letter in vowels_and_stress]
    res_li = li_pattern[1:]
    return "".join([str(symbol) for symbol in res_li])
    

# принимает словарь вида {слово с ударением : слово без ударения}
# возвращает словарь вида {шаблон слова : список подходящих слов}
def dct_pattern_words(dct_words):
    li_stresses = [stress_pattern(value) for value in dct_words.values()]
    all_patterns = list(set(li_stresses))
    pattern_word = {}
    for pattern in all_patterns:
        words = [word for word, stressed in dct_words.items() if stress_pattern(stressed) == pattern]
        pattern_word[pattern] = words
    with open('C:/Users/сергей/OneDrive/Рабочий стол/test2.txt', "w", encoding="utf-8") as f:
        json.dump(pattern_word, f, ensure_ascii=False)
    return pattern_word



cyr_symbols = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя́")
one_symb_word = set("аиоукясв")

    
