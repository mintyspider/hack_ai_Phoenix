import requests
import pyodbc


def update_property(db_path, table_name, row_id, column, value):
     '''
    Функция для обновления значения в базе данных Microsoft Access.

    Эта функция подключается к базе данных, обновляет указанное значение в заданном столбце для строки с определённым ID.

    Параметры:
    - db_path (str): Путь к базе данных Access.
    - table_name (str): Название таблицы, в которой будет происходить обновление данных.
    - row_id (int): Идентификатор строки, в которой необходимо обновить данные.
    - column (str): Название столбца, значение которого нужно обновить.
    - value (str): Новое значение для указанного столбца.

    Возвращаемое значение:
    - None. Функция выполняет операцию обновления данных в базе и сохраняет изменения.
    '''

    conn_str = (
        r"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};"
        r"DBQ={};".format(db_path)
    )

    conn = pyodbc.connect(conn_str)

    cursor = conn.cursor()

    update_query = f"UPDATE {table_name} SET {column} = ? WHERE ID = ?"
    cursor.execute(update_query, (value, row_id))


    conn.commit()


    cursor.close()
    conn.close()

def query_database(db_path, query):
    '''
       Функция для выполнения SQL-запроса к базе данных Access и получения результата.

       Эта функция подключается к базе данных, выполняет переданный SQL-запрос и возвращает результат в виде списка строк.

       Параметры:
       - db_path (str): Путь к базе данных Access.
       - query (str): SQL-запрос для выполнения.

       Возвращаемое значение:
       - rows (list): Список строк, полученных в результате выполнения SQL-запроса.
       '''
    conn_str = (
        r"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};"
        r"DBQ={};".format(db_path)
    )

    conn = pyodbc.connect(conn_str)

    # Создание курсора для выполнения SQL-запросов
    cursor = conn.cursor()


    cursor.execute(query)


    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def fill_properties_cells(db_path1, db_path2, query1, query2, param_query, text_file, table_name,parametrs_table_name):
    '''
        Основная функция для сравнения данных из двух баз данных и обновления свойств.

        Функция извлекает данные из двух баз данных Access, сравнивает строки на основе идентификаторов, и обновляет столбцы с найденными свойствами из текстового файла.

        Параметры:
        - db_path1 (str): Путь к первой базе данных.
        - db_path2 (str): Путь ко второй базе данных.
        - query1 (str): SQL-запрос для извлечения данных из первой базы.
        - query2 (str): SQL-запрос для извлечения данных из второй базы.
        - param_query (str): SQL-запрос для извлечения параметров из второй базы данных.
        - text_file (str): Путь к текстовому файлу, содержащему данные для сравнения.
        - table_name (str): Название таблицы, в которой будут обновляться свойства.
        - parametrs_table_name (str): Название таблицы с параметрами, которые будут обновляться.

        Возвращаемое значение:
        - None. Функция выполняет обновление данных в обеих базах данных.
        '''
    # Выполнение запроса к первой базе данных(для формирования таблицы ХАРАКТЕРИСТИКИ_ТОВАРОВ(групп) )
    rows1 = query_database(db_path1, query1)

    # Выполнение запроса ко второй базе данных(для таблицы СВОЙСТВА_ТОВАРОВ)
    rows2 = query_database(db_path2, query2)

    # Получение параметров из второй базы данных
    parametrs = query_database(db_path2, param_query)

    with open(text_file) as file:
        units_text = file.readlines()

    for row_id_groups in range(len(rows1)):
        for row_id in range(len(rows2)):
            if rows2[row_id][:6] == rows1[row_id_groups]:
                split_parametrs = parametrs[row_id].split()
                # Пример обработки параметров [38Л, П/Э]
                for item in split_parametrs:
                    for unit in units_text:
                        temp_unit = unit.split()
                        if temp_unit[2].find(item):
                            # Столбцы для проверки
                            columns = ["СВОЙСТВО1", "СВОЙСТВО2", "СВОЙСТВО3", "СВОЙСТВО4,СВОЙСТВО5", "СВОЙСТВО6", "СВОЙСТВО7", "СВОЙСТВО8","СВОЙСТВО9", "СВОЙСТВО10"]

                            # Проверка, какой столбец свободен
                            for column in columns:
                                check_query = f"SELECT {column} FROM {table_name} WHERE ID = ?"

                                conn_str = (
                                    r"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};"
                                    r"DBQ={};".format(db_path2)
                                )
                                conn = pyodbc.connect(conn_str)
                                cursor = conn.cursor()
                                cursor.execute(check_query, (row_id,))
                                result = cursor.fetchone()

                                if result and result[0] is None:
                                    update_property(db_path2, table_name, row_id, column, rows1[row_id_groups])
                                    update_property(db_path1,parametrs_table_name,row_id,column,item)
                                    break

                                cursor.close()
                                conn.close()



def main():
    # Пример использования функции с параметрами(т.к. это концепт кода)
    db_path1 = r"C:\path\to\first_database.accdb"
    db_path2 = r"C:\path\to\second_database.accdb"
    query1 = "SELECT * FROM OKPD_2"
    query2 = "SELECT * FROM OKPD_2"
    param_query = "SELECT * FROM Parametrs"
    text_file = "1.txt"
    table_name = "Parametrs"
    parametrs_table_name = "Properties"
    fill_properties_cells(db_path1, db_path2, query1, query2, param_query, text_file, table_name,parametrs_table_name)

if __name__ == "__main__":
    main()