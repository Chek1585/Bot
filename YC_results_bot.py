import mysql.connector
import re
import telebot
from telebot import types

def read_db_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key.strip()] = value.strip()
    return config

def connect_to_database(config):
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None

def get_top_10_users(cursor):
    query = "SELECT email, search_counter FROM user_results ORDER BY search_counter DESC LIMIT 10"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def get_top_10_words(cursor):
    cursor.execute("SELECT search_results FROM user_results")
    all_descriptions = cursor.fetchall()
    
    word_count = {}
    for description in all_descriptions:
        if description[0] is not None:
            words = re.findall(r'\b\w+\b', description[0].lower())
            for word in words:
                if word not in word_count:
                    word_count[word] = 0
                word_count[word] += 1
    
    sorted_words = sorted(word_count.items(), key=lambda item: item[1], reverse=True)
    return sorted_words[:10]

def get_top_10_titles(cursor):
    query = """
    SELECT title, COUNT(*) as count FROM (
        SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(lover_title, ',', numbers.n), ',', -1)) AS title
        FROM (
            SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10
            UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20
        ) numbers INNER JOIN user_results
        ON CHAR_LENGTH(lover_title) - CHAR_LENGTH(REPLACE(lover_title, ',', '')) >= numbers.n - 1
        WHERE TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(lover_title, ',', numbers.n), ',', -1)) != ''
    ) AS titles
    GROUP BY title
    HAVING title NOT IN ('', "''", "'", ",")
    ORDER BY count DESC
    LIMIT 10
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def get_top_10_genres(cursor):
    query = """
    SELECT genre, COUNT(*) as count FROM (
        SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(lover_genres, ',', numbers.n), ',', -1)) AS genre
        FROM (
            SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10
            UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20
        ) numbers INNER JOIN user_results
        ON CHAR_LENGTH(lover_genres) - CHAR_LENGTH(REPLACE(lover_genres, ',', '')) >= numbers.n - 1
        WHERE TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(lover_genres, ',', numbers.n), ',', -1)) != ''
    ) AS genres
    GROUP BY genre
    HAVING genre NOT IN ('', "''", "'", ",")
    ORDER BY count DESC
    LIMIT 10
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def get_top_10_actors(cursor):
    query = """
    SELECT actor, COUNT(*) as count FROM (
        SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(lover_cast, ',', numbers.n), ',', -1)) AS actor
        FROM (
            SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10
            UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15 UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20
        ) numbers INNER JOIN user_results
        ON CHAR_LENGTH(lover_cast) - CHAR_LENGTH(REPLACE(lover_cast, ',', '')) >= numbers.n - 1
        WHERE TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(lover_cast, ',', numbers.n), ',', -1)) != ''
    ) AS actors
    GROUP BY actor
    HAVING actor NOT IN ('', "''", "'", ",")
    ORDER BY count DESC
    LIMIT 10
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return results

bot = telebot.TeleBot('7281476762:AAEYBplqEEnapgNQ-2fbTSaZEFmdhev-Xnw')

@bot.message_handler(commands=['start'])
def start_message(message):
    show_main_menu(message.chat.id)

def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Топ 10 пользователей', 'Топ 10 слов', 'Топ 10 фильмов', 'Топ 10 жанров', 'Топ 10 актеров', 'Выход')
    bot.send_message(chat_id, 'Выберите действие:', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_db_config = read_db_config('users_result.txt')
    connection = connect_to_database(user_db_config)
    cursor = connection.cursor()

    if message.text == 'Топ 10 пользователей':
        top_users = get_top_10_users(cursor)
        response = "Топ 10 самых активных пользователей:\n"
        for idx, user in enumerate(top_users, start=1):
            response += f"{idx}. Email: {user[0]}, Количество поисков: {user[1]}\n"
        bot.send_message(message.chat.id, response)

    elif message.text == 'Топ 10 слов':
        top_words = get_top_10_words(cursor)
        response = "Топ 10 самых часто используемых слов из краткого описания:\n"
        for idx, (word, count) in enumerate(top_words, start=1):
            if word not in ["'", ",", "''"]:
                response += f"{idx}. Слово: {word}, Количество: {count}\n"
        bot.send_message(message.chat.id, response)

    elif message.text == 'Топ 10 фильмов':
        top_titles = get_top_10_titles(cursor)
        response = "Топ 10 самых любимых фильмов:\n"
        for idx, title in enumerate(top_titles, start=1):
            if title[0] not in ["", "''", "'", ","]:
                response += f"{idx}. Название: {title[0]}, Количество: {title[1]}\n"
        bot.send_message(message.chat.id, response)

    elif message.text == 'Топ 10 жанров':
        top_genres = get_top_10_genres(cursor)
        response = "Топ 10 самых любимых жанров:\n"
        for idx, genre in enumerate(top_genres, start=1):
            if genre[0] not in ["", "''", "'", ","]:
                response += f"{idx}. Жанр: {genre[0]}, Количество: {genre[1]}\n"
        bot.send_message(message.chat.id, response)

    elif message.text == 'Топ 10 актеров':
        top_actors = get_top_10_actors(cursor)
        response = "Топ 10 самых любимых актеров:\n"
        for idx, actor in enumerate(top_actors, start=1):
            if actor[0] not in ["", "''", "'", ","]:
                response += f"{idx}. Актер: {actor[0]}, Количество: {actor[1]}\n"
        bot.send_message(message.chat.id, response)

    elif message.text == 'Выход':
        bot.send_message(message.chat.id, "Выход из системы. Нажмите /start для нового сеанса.")
        return

    else:
        bot.send_message(message.chat.id, "Неверный выбор, попробуйте снова.")

    cursor.close()
    connection.close()

    # Показать меню снова
    show_main_menu(message.chat.id)

bot.polling(none_stop=True)













