

import sqlite3

DB_NAME = 'database.db'
table_name = 'texts'
# Функция для подключения к базе данных или создания новой, если её ещё нет
def prepare_db():
    create_db()
    create_table()

def create_db(database_name=DB_NAME):
    connection = sqlite3.connect(database_name)
    connection.close()
# Функция для выполнения любого sql-запроса для изменения данных
# Получает sql-запрос и выполняет его
def execute_query(sql_query, data=None, db_path=DB_NAME):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        if data:
            cursor.execute(sql_query, data)
        else:
            cursor.execute(sql_query)
        connection.commit()
    # Функция для выполнения любого sql-запроса для получения данных (возвращает значение)
def execute_selection_query(sql_query, data=None, db_path=DB_NAME):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    if data:
        cursor.execute(sql_query, data)
    else:
        cursor.execute(sql_query)
    rows = cursor.fetchall()
    connection.close()
    return rows
# Функция для создания новой таблицы (если такой ещё нет)
# Получает название и список колонок в формате ИМЯ: ТИП
# Создаёт запрос CREATE TABLE IF NOT EXISTS имя_таблицы (колонка1 ТИП, колонка2 ТИП)
def create_table():
    sql_query = (f'''CREATE TABLE IF NOT EXISTS {table_name} ( 
                 id INTEGER PRIMARY KEY, 
                 message_text TEXT, 
                 tts_symbols INTEGER, 
                 stt blocks INTEGER)''')
    execute_query(sql_query)
# Функция для вставки новой строки в таблицу
def insert_row(user_id, message, tts_symbols, table_name=f'{table_name}'):
    sql_query = f'INSERT INTO {table_name}(user_id, message, tts_symbols) VALUES (?, ?, ?)'
    execute_query(sql_query, [user_id, message, tts_symbols])
# Функция для подсчёта израсходованных символов для одного пользователя
def count_all_symbol(user_id):
    sql_query = f'SELECT SUM(tts_symbols) FROM texts WHERE user_id = ?'
    data = execute_selection_query(sql_query, [user_id])[0]
    if data and data[0]:
        return data[0]  # Если результат есть и data[0] == какому-то числу, то
        # возвращаем это число - сумму всех потраченных символов
    else:
        return 0  # Результата нет, так как у нас ещё нет записей о потраченых символах
        # возвращаем 0
# Функция для подготовки базы данных
# Создаёт/подключается к бд, создаёт таблицу
