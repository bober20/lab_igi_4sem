import re
import zipfile
from task2 import file_service


class TextAnalysis:

    def __init__(self):
        self.service = file_service.FileService()

        self.text_from_file = self.service.read_text_from_file()


    def print_result(self):
        """This function prints result."""

        result = self.return_results_from_all_functions()

        for i in result:
            print(i, '\n')

        self.service.write_results_to_file(result=result)
        self.service.make_zip()
        print("Inner files info.")
        self.service.get_inner_files_info()


    def return_results_from_all_functions(self):
        """This function returns result from all functions."""

        result = list()

        result.append(self.find_telephone_numbers())
        result.append(self.find_words_2_3_characters_determined())
        result.append(self.count_space_separated_words())
        result.append(self.count_same_letter())
        result.append(self.find_collocations())
        result.append(self.count_sentences())
        result.append(self.count_sentences_type())
        result.append(self.average_sentence_length())
        result.append(self.average_word_length())
        result.append(self.count_smileys())

        return result

    def find_telephone_numbers(self):
        """This function counts telephone numbers and returns all of them."""

        phone_regex = r'\b29\d{7}\b'
        phones = re.findall(phone_regex, self.text_from_file)

        return phones

    def find_words_2_3_characters_determined(self):
        """This function returns all words that contain determined characters."""

        word_regex = r'\w\w*[\s.:?!,]'
        determined_word_regex = r'\w[^aeiouAEIOU][aeiouAEIOU]\w*'

        words = re.findall(word_regex, self.text_from_file)
        result_words = list()

        for i in words:
            result = re.match(determined_word_regex, i)

            if result is None:
                continue

            result_words.append(result.group(0))

        return result_words

    def count_space_separated_words(self):
        """This function counts space separated words."""

        word_regex = r'\s\w+\s'

        string = self.text_from_file
        result = list()

        while True:
            word = re.search(word_regex, string)

            if not word:
                break

            string = string[word.end()-1:]

            result.append(word.group(0))

        return len(result)

    def count_same_letter(self):
        """This function counts number of each letter."""

        letter_count = {}

        # Находим все буквы в строке
        letters = re.findall(r'[a-zA-Z]', self.text_from_file)

        # Подсчитываем количество каждой буквы
        for letter in letters:
            if letter in letter_count:
                letter_count[letter] += 1
            else:
                letter_count[letter] = 1

        return letter_count

    def find_collocations(self):
        """This function fins all collocations."""

        collocation_regex = r'\b\w+(?:\s+\w+)*\b'
        phrases = re.findall(collocation_regex, self.text_from_file)  # Находим все словосочетания в тексте
        sorted_phrases = sorted(phrases)  # Сортируем словосочетания по алфавиту

        return ", ".join(sorted_phrases)  # Объединяем отсортированные словосочетания снова с запятыми

    def count_sentences(self):
        """This function counts sentences."""

        sentence_regex = r'[.!?](?:\s|$)'
        sentences = re.findall(sentence_regex, self.text_from_file)

        return len(sentences)

    def count_sentences_type(self):
        """This function counts sentences of 3 types."""

        narr_count = len(re.findall(r'\w+[.]', self.text_from_file))  # Повествовательные предложения
        interrogate_count = len(re.findall(r'\w+[?]', self.text_from_file))  # Вопросительные предложения
        imper_count = len(re.findall(r'\w+!', self.text_from_file))  # Побудительные предложения

        return narr_count, interrogate_count, imper_count

    def average_sentence_length(self):
        """This function calculates average sentence's length."""

        sentences = re.findall(r'\b\w[\w\s]*?[.!?]', self.text_from_file)  # Разделение текста на предложения
        total_characters = sum(len(sentence.replace(' ', '')) for sentence in sentences)  # Общее количество символов
        # в предложениях
        total_sentences = len(sentences)  # Общее количество предложений

        if total_sentences == 0:
            return 0

        average_length = total_characters / total_sentences  # Средняя длина предложения в символах

        return average_length

    def average_word_length(self):
        """This function calculates average word's length."""

        # Находим все слова в тексте
        words = re.findall(r'\b\w+\b', self.text_from_file)

        total_characters = sum(len(word) for word in words)
        total_words = len(words)

        if total_words == 0:
            return 0

        # Вычисляем среднюю длину слова
        average_length = total_characters / total_words

        return average_length

    def count_smileys(self):
        """This function calculates number of smileys."""

        smiley_regex = r'[:;]-*[\(\)\[\]]+'
        smileys = re.findall(smiley_regex, self.text_from_file)

        return len(smileys)





