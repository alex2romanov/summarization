

# import streamlit as st
# import sqlite3

# # Функция для создания таблицы в базе данных
# def create_table():
#     conn = sqlite3.connect('translations.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS translations
#                  (id INTEGER PRIMARY KEY, original_text TEXT, translated_text TEXT)''')
#     conn.commit()
#     conn.close()



# def print_first_10_texts():
#     # Подключение к базе данных
#     conn = sqlite3.connect('translations.db')
#     c = conn.cursor()

#     # Извлечение первых 10 записей из таблицы translations
#     c.execute('SELECT * FROM translations LIMIT 10')
#     rows = c.fetchall()

#     # Закрытие соединения
#     conn.close()

#     # Печать первых 10 текстов
#     for row in rows:
#         text = f"ID: {row[0]}, Original Text: {row[1]}, Translated Text: {row[2]}"
#         #print(f"ID: {row[0]}, Original Text: {row[1]}, Translated Text: {row[2]}")
#         st.write("Перевод:", text)

# # Вызов функции для печати первых 10 текстов


# # Функция для вставки перевода в базу данных
# def insert_translation(original_text, translated_text):
#     conn = sqlite3.connect('translations.db')
#     c = conn.cursor()
#     c.execute('INSERT INTO translations (original_text, translated_text) VALUES (?, ?)',
#               (original_text, translated_text))
#     conn.commit()
#     conn.close()

# # Создание таблицы при запуске
# create_table()

# # Заголовок приложения
# st.title("Приложение для перевода")

# # Ввод текста пользователем
# input_text = st.text_area("Введите текст для перевода:")

# # Кнопка для перевода текста
# if st.button("Перевести"):
#     # Пример перевода (замените этой функцией реальный перевод)
#     translated_text = input_text[::-1]  # Перевод - обратный порядок символов для примера

#     # Отображение перевода
#     st.write("Перевод:", translated_text)

#     # Запись перевода в базу данных
#     insert_translation(input_text, translated_text)
#     print_first_10_texts()

#     st.success("Перевод сохранен в базу данных!")

import streamlit as st
import sqlite3
from openai import OpenAI
import requests
from requests.auth import HTTPProxyAuth
import httpx


# Функция для обновления базы данных
def update_db():

    conn = sqlite3.connect('book_contents.db')
    c = conn.cursor()

    # Создание таблицы, если она еще не существует
    c.execute('''
    CREATE TABLE IF NOT EXISTS book_contents (
        name_book TEXT,
        id_chapter INTEGER,
        user_content TEXT
    )
    ''')
    conn.commit()
    conn.close()

def st_write_large_text(text):
    st.markdown(f'<div style="font-size: 36px;">{text}</div>', unsafe_allow_html=True)

# Использование функции для вывода текста

# Функция для получения краткого содержания из базы данных
def get_summary(id):
    conn = sqlite3.connect('summary_questions1.sqlite')
    c = conn.cursor()
    c.execute('SELECT chapter_summary FROM summary_questions WHERE id_chapter=?', (id,))
    summary = c.fetchone()
    conn.close()
    return summary[0] if summary else "Краткое содержание не найдено"

def get_questions(id):
    conn = sqlite3.connect('summary_questions1.sqlite')
    c = conn.cursor()
    c.execute('SELECT questions_summary FROM summary_questions WHERE id_chapter=?', (id,))
    summary = c.fetchone()
    conn.close()
    return summary[0] if summary else "Краткое содержание не найдено"

# Функция для сохранения пользовательского текста в базе данных

def add_content(name_book, id_chapter, user_content):
    conn = sqlite3.connect('book_contents.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO book_contents (name_book, id_chapter, user_content)
    VALUES (?, ?, ?)
    ''', (name_book, id_chapter, user_content))
    conn.commit()
    conn.close()

# Обновление базы данных перед запуском приложения
#update_db()

# Инициализация состояния
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False
    st.session_state.button_id = None

# Заголовок приложения
st.title('Краткое содержание книги "Коллектив авторов"')

# Функция для возврата к выбору кнопок
def reset():
    st.session_state.button_clicked = False
    st.session_state.button_id = None

# Отображение кнопок или краткого содержания в зависимости от состояния
if st.session_state.button_clicked:
    summary = get_summary(st.session_state.button_id)
    st.write(summary)
    st_write_large_text("Вам предлагается ответить на вопросы по краткому содержанию.")
    questions = get_questions(st.session_state.button_id)
    st.write(questions)
    user_input = st.text_area("Напишите ваш текст ниже:")
    if st.button('Сохранить текст'):
        add_content("Book1", st.session_state.button_id, user_input)
        st.success("Ваш текст был сохранен!")
        prompt_example = f'''Есть текст: {summary}. Я ответил на вопросы: {questions} следующим образом: 1. Существенное влияение. 2. Джеймс ввел значительный вклад.  3. Цель познакомить читателя с книгой. 4. Развитие это действие. Оцени ответ пользователя.'''
        
        proxies_list = [
        'http://130.180.208.145',
        'http://101.128.107.210',
        'http://102.215.198.113',
        'http://13.80.134.180',
        'http://13.37.28.247',
        'http://131.100.48.125',
        'http://136.226.255.23',
        'http://165.16.27.43',
        'http://166.159.90.56',
        'http://194.150.71.39',
        'http://177.93.36.151',
        ]
        def create_openai_client(proxy_url):
             return OpenAI(api_key=api_key, http_client=httpx.Client(proxies=proxy_url))

        for proxy in proxies_list:
            try:
                openai_client = create_openai_client(proxy)
        #client = OpenAI(api_key = api_key, http_client=httpx.Client(proxies="http://116.203.28.43"))
        # Configure your proxy

                response = client.chat.completions.create(
                    model="gpt-4o-mini", # Или gpt-4,
                    # в данной задаче грейдер не проверяет какую модель вы выбрали,
                    # но советуем попробовать gpt-4 в качестве экперимента.
                    messages=[
                        {
                            "role": "user",
                            "content": prompt_example,
                        }
                    ],
                    temperature=0.7  # Уровень случайности вывода модели
                )
                st.write(response.choices[0].message.content)
                break
            except:
                # Print the error and try the next proxy
                print(f"Failed with proxy {proxy}")
                continue


    if st.button('Вернуться к выбору кнопок'):
        reset()
else:
    if st.button('Глава 1: История исследований развития'):
        st.session_state.button_clicked = True
        st.session_state.button_id = 1
    elif st.button('Глава 2: Формы и области (сферы) развития'):
        st.session_state.button_clicked = True
        st.session_state.button_id = 2
    elif st.button('Глава 3: Цели развития'):
        st.session_state.button_clicked = True
        st.session_state.button_id = 3
    elif st.button('Глава 4: Цели психического развития. итоги'):
        st.session_state.button_clicked = True
        st.session_state.button_id = 4
    if st.button('Глава 5: Понятие факторов психического развития'):
        st.session_state.button_clicked = True
        st.session_state.button_id = 5

# Пояснительный текст
if not st.session_state.button_clicked:
    st.write('Нажмите на одну из кнопок выше, чтобы увидеть соответствующее краткое содержание.')
