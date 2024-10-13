import pyodbc
from sklearn.feature_extraction.text import TfidfVectorizer

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
db_path = '' # Внести свой путь нахождения бд
table_name = 'Группы'
source_column = 'Товар'
target_column = 'Группа'

extract_first_word(db_path, table_name, source_column, target_column)

# ***** #

# Улучшенная версия с использованием алгоритма TF-IDF

def choose_group_name(documents):
  
  # Создание объекта TfidfVectorizer
  tfidf_vectorizer = TfidfVectorizer()
  
  # Применение TF-IDF к текстовым данным
  tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
  
  # Получение списка ключевых слов и их значения TF-IDF для воды
  feature_names = tfidf_vectorizer.get_feature_names_out()
  tfidf_scores = tfidf_matrix.toarray()[0]
  
  # Сортировка слов по значениям TF-IDF
  sorted_keywords = [word for _, word in sorted(zip(tfidf_scores, feature_names), reverse=True)]
  
  group_name = sorted_keywords[0]
  return group_name
  
# Пример текстовых данных на основе воды
documents = [
  "ВОДА ПРИРОДНАЯ ПИТЬЕВАЯ АРТЕЗИАНСКАЯ ПЕРВОЙ КАТЕГОРИИ НЕГАЗИРОВАННАЯ",
  "ВОДА ПИТЬЕВАЯ",
  "ВОДА ЧИСТАЯ",
  "ВОДА ПИТЬЕВАЯ ПРИРОДНАЯ",
  "ВОДА ПИТЬЕВАЯ НЕГАЗИРОВАННАЯ",
  "ВОДА ПИТЬЕВАЯ ГАЗИРОВАННАЯ"
]
