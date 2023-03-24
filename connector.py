import json


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        try:
            with open(self.__data_file, "r", encoding='utf-8') as f:
                json.load(f)
        except FileNotFoundError:
            with open(self.__data_file, "w", encoding='utf-8') as f:
                json.dump([], f,)
        except json.JSONDecodeError:
            raise Exception("Json файл поврежден")

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        data = json.dumps(data, indent=2, ensure_ascii=False)
        with open(self.__data_file, "w", encoding='utf-8') as f:
            f.write(data)

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        with open(self.__data_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            f.close()
        if not len(query):
            return existing_data

        data_from_file = []
        for item in existing_data:
            for key, value in query.items():
                if item[key] == value:
                    data_from_file.append(item)
        return data_from_file

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if not len(query):
            return
        with open(self.__data_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            f.close()
        with open(self.__data_file, 'w', encoding='utf-8') as f:
            existing_data = list(
                filter(lambda item: not all(item[key] == value for key, value in query.items()), existing_data))

            json.dump(existing_data, f, indent=2, ensure_ascii=False)
            f.close()
