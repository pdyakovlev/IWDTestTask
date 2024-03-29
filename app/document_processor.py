import math
import re


class DocumentProcessor:
    """Обработчик документов. Вызовите метод process_doc
    для получения обработанного документа."""
    def __init__(self, document) -> None:
        self.document = document

    def process_doc(self):
        """Метод обработки документа"""
        if self.document is None:
            return None
        doc = self.document.read()
        try:
            unicode_doc = doc.decode('utf-8')
        except Exception:
            return 'Возникло исключение, проверьте формат документа.'
        # получаем лист документов, каждый документ - строка
        docs: list = self.__get_documents__(unicode_doc)
        word_tf_total: dict = {}
        words_total: list = []
        for document in docs:
            words_total += self.__separate_string__(document)
            # получаем tf для слов в документе
            document_tf: list = self.__get_tf__(document)
            for word_tf in document_tf:
                for word, tf in word_tf.items():
                    # записываем в общий словарь
                    if word in word_tf_total.keys():
                        word_tf_total[word] = round(
                            ((tf+word_tf_total[word])/2),
                            3)
                    else:
                        word_tf_total[word] = tf
        word_idf: dict = self.__get_idf__(words_total, docs)
        result: list = self.__get_result__(word_tf_total, word_idf)
        return result[:50]

    def __get_tf__(self, words: str) -> list:
        """Метод получения TF."""
        word_tf: list = []
        separated_words: list = self.__separate_string__(words)
        word_count: dict = self.__get_word_count__(separated_words)
        words_total: int = len(separated_words)
        for word, count in word_count.items():
            word_tf.append({word: round(count/words_total, 3)})
        return word_tf

    def __get_idf__(self, words: str, docs: list) -> dict:
        """Метод получения IDF."""
        set_words = set(words)
        word_in_docs: dict = {}
        word_idf: dict = {}
        docs_count: int = len(docs)
        for word in set_words:
            for doc in docs:
                if word in doc:
                    if word_in_docs.get(word, None):
                        word_in_docs[word] += 1
                    else:
                        word_in_docs[word] = 1
        for word in set_words:
            word_idf[word] = round(math.log(docs_count / word_in_docs[word]),
                                   3)
        return word_idf

    def __to_words__(self, string_doc):
        """Метод, возвращающий разделённую на слова строку."""
        words: list = self.separate_string(string_doc)
        return words

    def __get_word_count__(self, words: list) -> dict:
        """Метод, возвращающий количество вхождений слова
        в текст отдельного документа."""
        word_count: dict = {}
        for word in words:
            if word_count.get(word, None):
                word_count[word] += 1
            else:
                word_count[word] = 1
        return word_count

    def __get_documents__(self, string_file: str) -> list:
        """Метод, разбивающий общий файл на отдельные документы."""
        docs = self.__separate_string__(string_file, '@doc')
        return docs

    def __separate_string__(self, string: str, separator=None) -> list:
        """Метод, разбивающий строку по переданному разделителю
        и убирающий спецсимволы."""
        string: str = string.lower()
        cleaned_string: str = re.sub(r'(?<!@)@[^\w\s-]|[\d.,"%«»]', '', string)
        separated: list = cleaned_string.split(separator)
        return separated

    def __get_result__(self, word_tf: dict, word_idf: dict) -> list:
        """Метод, сводящий все данные в один лист."""
        sort_word_idf: dict = dict(sorted(
            word_idf.items(),
            key=lambda item: item[1],
            reverse=True))

        word_tf_idf: list = []
        for word, idf in sort_word_idf.items():
            word_tf_idf.append([word, word_tf[word], idf])
        return word_tf_idf
