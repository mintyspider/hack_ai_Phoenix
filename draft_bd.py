import pyodbc

# Путь к файлу базы данных Access
db_path = r"C:\Users\Анастасия\OneDrive\Документы\GitHub\hack_ai_Phoenix\database.accdb"  # Измените путь на свой

# Строка подключения к Access базе данных
conn_str = (
    r"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};"
    r"DBQ={};".format(db_path)
)
conn = pyodbc.connect(conn_str)

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Пример SQL-запроса для выборки всех данных из таблицы
query = "SELECT * FROM OKPD_2"
cursor.execute(query)

# Извлечение всех данных из запроса
rows = cursor.fetchall()

# Обработка данных
for row in rows:
    print(row)

# Закрытие подключения
cursor.close()
conn.close()
