class ProductGroup:
    def __init__(self, code, name):
        self.code = code  # Код товара
        self.name = name  # Название группы товаров
        self.properties = []  # Список свойств

    def add_property(self, property_name):
        if len(self.properties) < 10:  # Ограничение не более 10 свойств
            self.properties.append(property_name)
        else:
            print(f"Нельзя добавить больше 10 свойств для группы {self.name}.")

    def display(self):
        print(f"Группа товаров: {self.name} (Код: {self.code})")
        for i, prop in enumerate(self.properties, start=1):
            print(f"  Свойство {i}: {prop}")


class Classification:
    def __init__(self):
        self.groups = {}  # Словарь для хранения групп товаров по коду

    def add_group(self, code, name):
        if code not in self.groups:
            self.groups[code] = ProductGroup(code, name)
        else:
            print(f"Группа с кодом {code} уже существует.")

    def add_property_to_group(self, code, property_name):
        if code in self.groups:
            self.groups[code].add_property(property_name)
        else:
            print(f"Группа с кодом {code} не найдена.")

    def display(self):
        for group in self.groups.values():
            group.display()


# Пример использования
classification = Classification()

# Добавляем группы товаров
classification.add_group('01.01', 'Первая группа товаров')
classification.add_group('01.02', 'Вторая группа товаров')
classification.add_group('01.03', 'Третья группа товаров')

# Добавляем свойства к группам
classification.add_property_to_group('01.01', 'Свойство 1')
classification.add_property_to_group('01.01', 'Свойство 2')
