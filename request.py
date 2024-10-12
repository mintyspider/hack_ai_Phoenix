import pyodbc
from kanren import Relation, facts, var, run, conde
from sympy import symbols

item_type = GetItemType()
connect_str = (r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
               r"DBQ=C:\Users\user\Downloads\Справочник товаров.accdb;")

conn = pyodbc.connect(connect_str)

cursor = conn.cursor()

# запрос для получения всех данных из таблицы "item_type"
query = f"SELECT * FROM {item_type}"
cursor.execute(query)

# строки таблицы "item_type"
rows = cursor.fetchall()

cursor.close()
conn.close()

# отношение для названий и свойств
items_relation = Relation()

# добавляем названия товаров и их свойства
facts(items_relation, *rows)

# извлекаем все свойства из таблицы для проверки
all_properties = set()
for row in rows:
    all_properties.update(row)

# считывание свойств с проверкой
input_properties = []
while True:
    property_value = input("Введите свойство или 'стоп' для завершения: ")
    if property_value.lower() == 'стоп':
        break
    if property_value not in all_properties:
        print(f"Не найдено соответствующее свойство: {property_value}")
    else:
        input_properties.append(property_value)

x = var()  # переменная для сравнения свойств

def properties_compare(*properties):
    x = var()
    rule = conde(
        (items_relation(x, *properties),)
    )
    return run(0, x, rule)  # если это возвращает список, то это наши товары

# наши товары
results = run(0, x, (items_relation, x, *input_properties))

if results:
    print("Товары, соответствующие заданным свойствам:")
    for result in results:
        print(result)
else:
    print("Не найдено товаров, соответствующих введенным свойствам.")
