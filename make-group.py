import pyodbc

# Функция для подключения к базе данных Access
def connect_to_access_db(db_path):
    conn_str = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=" + db_path + ";"
    )
    conn = pyodbc.connect(conn_str)
    return conn

# Функция для вычленения первого слова и записи в новый столбец
def extract_first_word(db_path, table_name, source_column, target_column):
    # Подключаемся к базе данных
    conn = connect_to_access_db(db_path)
    cursor = conn.cursor()

    # Проверяем, существует ли уже целевой столбец
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [column[0] for column in cursor.description]
    if target_column not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {target_column} TEXT")

    # Извлекаем данные и обновляем новый столбец
    cursor.execute(f"SELECT id, {source_column} FROM {table_name}")
    rows = cursor.fetchall()

    for row in rows:
        record_id = row[0]
        first_word = row[1].split()[0] if row[1] else ""
        
        # Обновляем целевой столбец
        cursor.execute(f"UPDATE {table_name} SET {target_column} = ? WHERE id = ?", (first_word, record_id))

    # Сохраняем изменения
    conn.commit()
    conn.close()

# Пример использования
db_path = '' # Поменять на свой путь нахождения бд
table_name = 'Группы'
source_column = 'Товар'
target_column = 'Группа'

extract_first_word(db_path, table_name, source_column, target_column)
