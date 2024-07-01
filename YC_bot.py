import mysql.connector
from datetime import datetime
import uuid
import telebot
from telebot import types
from googletrans import Translator

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

def translate_text(text, dest_language):
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text

def get_language_code(language):
    if language == 'Русский':
        return 'ru'
    elif language == 'Deutsch':
        return 'de'
    else:
        return 'en'

bot = telebot.TeleBot('7361708872:AAGROSJksRsoUOwk_GHSEnpv8cCNKnhZa3g')
language = ''
email = ''
user_name = ''
search_params = {}
offset = 0

YEAR_RANGE = (2013, 2015)
DURATION_RANGE = (6, 196)
RATING_RANGE = (1.6, 9.4)

PROMPT_YEAR = {
    'Русский': 'Выберите тип сравнения для года выпуска (1: >, 2: < , 3: =, 4: оставить по умолчанию): ',
    'English': 'Choose the comparison type for the year of release (1: >, 2: <, 3: =, 4: leave default): ',
    'Deutsch': 'Wählen Sie den Vergleichstyp für das Veröffentlichungsjahr (1: >, 2: <, 3: =, 4: Standard belassen): '
}

PROMPT_DURATION = {
    'Русский': 'Выберите тип сравнения для продолжительности фильма (1: >, 2: < , 3: =, 4: оставить по умолчанию): ',
    'English': 'Choose the comparison type for the movie duration (1: >, 2: <, 3: =, 4: leave default): ',
    'Deutsch': 'Wählen Sie den Vergleichstyp für die Filmlänge (1: >, 2: <, 3: =, 4: Standard belassen): '
}

PROMPT_RATING = {
    'Русский': 'Выберите тип сравнения для рейтинга фильма (1: >, 2: < , 3: =, 4: оставить по умолчанию): ',
    'English': 'Choose the comparison type for the movie rating (1: >, 2: <, 3: =, 4: leave default): ',
    'Deutsch': 'Wählen Sie den Vergleichstyp für die Filmbewertung (1: >, 2: <, 3: =, 4: Standard belassen): '
}

PROMPT_COMPARISON = {
    'Русский': 'Выберите тип сравнения (>, < или =): ',
    'English': 'Choose the comparison type (>, <, or =): ',
    'Deutsch': 'Wählen Sie den Vergleichstyp (>, < oder =): '
}

COMPARISON_OPTIONS = {
    'Русский': {'1': '>', '2': '<', '3': '=', '4': ''},
    'English': {'1': '>', '2': '<', '3': '=', '4': ''},
    'Deutsch': {'1': '>', '2': '<', '3': '=', '4': ''}
}

PROMPT_GENRE = {
    'Русский': 'Введите жанр(ы) через запятую (или 4: не важно): ',
    'English': 'Enter genre(s) separated by commas (or 4: does not matter): ',
    'Deutsch': 'Geben Sie Genre(s) durch Kommas getrennt ein (oder 4: egal): '
}

PROMPT_ACTOR = {
    'Русский': 'Введите любимого артиста(ов) через запятую (или 4: не важно): ',
    'English': 'Enter favorite actor(s) separated by commas (or 4: does not matter): ',
    'Deutsch': 'Geben Sie Lieblingsschauspieler durch Kommas getrennt ein (oder 4: egal): '
}

PROMPT_TITLE = {
    'Русский': 'Введите название фильма (или 4: не важно): ',
    'English': 'Enter the movie title (or 4: does not matter): ',
    'Deutsch': 'Geben Sie den Filmtitel ein (oder 4: egal): '
}

PROMPT_DESCRIPTION = {
    'Русский': 'Введите ключевые слова описания через запятую (или 4: не важно): ',
    'English': 'Enter description keywords separated by commas (or 4: does not matter): ',
    'Deutsch': 'Geben Sie Beschreibungsschlüsselwörter durch Kommas getrennt ein (oder 4: egal): '
}

PROMPT_LANGUAGE = {
    'Русский': 'Введите язык фильма (или 4: не важно): ',
    'English': 'Enter the movie language (or 4: does not matter): ',
    'Deutsch': 'Geben Sie die Filmsprache ein (oder 4: egal): '
}

PROMPT_NEXT_ACTION = {
    'Русский': 'Введите 1 для просмотра следующих 10 фильмов, 2 для нового поиска или 3 для завершения: ',
    'English': 'Enter 1 to view the next 10 movies, 2 to start a new search, or 3 to end: ',
    'Deutsch': 'Geben Sie 1 ein, um die nächsten 10 Filme anzuzeigen, 2, um eine neue Suche zu starten, oder 3, um zu beenden: '
}

RESULTS_HEADER = {
    'Русский': 'Найденные фильмы (общее количество по данному поиску: {}):',
    'English': 'Found movies (total for this search: {}):',
    'Deutsch': 'Gefundene Filme (gesamt für diese Suche: {}):'
}

RESULTS_FORMAT = {
    'Русский': "Название: {}, Год выпуска: {}, Жанры: {}, Рейтинг: {}",
    'English': "Title: {}, Year: {}, Genres: {}, Rating: {}",
    'Deutsch': "Titel: {}, Jahr: {}, Genres: {}, Bewertung: {}"
}

RESULTS_POSTER = {
    'Русский': "Постер: {}",
    'English': "Poster: {}",
    'Deutsch': "Poster: {}"
}

messages = {
    'Русский': {
        'email_prompt': "Введите вашу электронную почту: ",
        'invalid_email': "Некорректный формат электронной почты. Пожалуйста, введите еще раз.",
        'name_prompt': "Введите ваше имя, если оставите пустым, будет использовано 'user': ",
        'registration_offer': "Хотите зарегистрироваться для получения обновлений и скидок?",
        'parameter_choice': "Выберите параметр поиска или начните поиск:",
        'user_exists': "Пользователь уже существует в базе данных.",
        'user_added': "Пользователь успешно добавлен в базу данных.",
        'search_complete': "Поиск завершен. Нажмите /start чтобы начать заново.",
        'invalid_choice': "Неверный выбор. Пожалуйста, попробуйте еще раз.",
        'yes': 'Да',
        'no': 'Нет',
        'year': 'Год выпуска',
        'duration': 'Продолжительность',
        'rating': 'Рейтинг',
        'genre': 'Жанр',
        'actor': 'Любимый артист',
        'title': 'Название',
        'description': 'Описание',
        'language': 'Язык',
        'start_search': 'Начать поиск'
    },
    'English': {
        'email_prompt': "Enter your email: ",
        'invalid_email': "Invalid email format. Please try again.",
        'name_prompt': "Enter your name, if left empty, 'user' will be used: ",
        'registration_offer': "Do you want to register for updates and discounts?",
        'parameter_choice': "Choose a search parameter or start the search:",
        'user_exists': "User already exists in the database.",
        'user_added': "User successfully added to the database.",
        'search_complete': "Search complete. Press /start to start again.",
        'invalid_choice': "Invalid choice. Please try again.",
        'yes': 'Yes',
        'no': 'No',
        'year': 'Year of release',
        'duration': 'Duration',
        'rating': 'Rating',
        'genre': 'Genre',
        'actor': 'Favorite actor',
        'title': 'Title',
        'description': 'Description',
        'language': 'Language',
        'start_search': 'Start search'
    },
    'Deutsch': {
        'email_prompt': "Geben Sie Ihre E-Mail-Adresse ein: ",
        'invalid_email': "Ungültiges E-Mail-Format. Bitte versuchen Sie es erneut.",
        'name_prompt': "Geben Sie Ihren Namen ein, wenn Sie ihn leer lassen, wird 'user' verwendet: ",
        'registration_offer': "Möchten Sie sich für Updates und Rabatte registrieren?",
        'parameter_choice': "Wählen Sie einen Suchparameter oder starten Sie die Suche:",
        'user_exists': "Benutzer existiert bereits in der Datenbank.",
        'user_added': "Benutzer erfolgreich in die Datenbank aufgenommen.",
        'search_complete': "Suche abgeschlossen. Drücken Sie /start, um erneut zu beginnen.",
        'invalid_choice': "Ungültige Wahl. Bitte versuchen Sie es erneut.",
        'yes': 'Ja',
        'no': 'Nein',
        'year': 'Jahr der Veröffentlichung',
        'duration': 'Dauer',
        'rating': 'Bewertung',
        'genre': 'Genre',
        'actor': 'Lieblingsschauspieler',
        'title': 'Titel',
        'description': 'Beschreibung',
        'language': 'Sprache',
        'start_search': 'Suche starten'
    }
}

@bot.message_handler(commands=['start'])
def start_message(message):
    global offset
    offset = 0
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('1', '2', '3')
    bot.send_message(message.chat.id, '''  
    Выберите язык интерфейса (Choose language): 
    для русского - 1, for English - 2, für Deutsch - 3
    ''', reply_markup=markup)
    bot.register_next_step_handler(message, get_language)

def get_language(message):
    global language
    if message.text == '1':
        language = 'Русский'
        message_us = 'Вы выбрали язык: Русский'
    elif message.text == '2':
        language = 'English'
        message_us = 'You chose the language: English'
    elif message.text == '3':
        language = 'Deutsch'
        message_us = 'Sie haben die Sprache gewählt: Deutsch'
    else:
        bot.send_message(message.chat.id, "Неверный выбор языка. Пожалуйста, попробуйте еще раз.")
        bot.register_next_step_handler(message, get_language)
        return

    bot.send_message(message.chat.id, message_us)
    offer_registration(message)

def offer_registration(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(messages[language]['yes'], messages[language]['no'])
    bot.send_message(message.chat.id, messages[language]['registration_offer'], reply_markup=markup)
    bot.register_next_step_handler(message, handle_registration_offer)

def handle_registration_offer(message):
    if message.text.lower() == messages[language]['yes'].lower():
        get_user_info(message)
    else:
        show_main_menu(message)

def get_user_info(message):
    bot.send_message(message.chat.id, messages[language]['email_prompt'])
    bot.register_next_step_handler(message, validate_email)

def validate_email(message):
    global email
    email = message.text.strip()
    if '@' in email and '.' in email:
        user_db_config = read_db_config('users_result.txt')
        connection = connect_to_database(user_db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM user_results WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result[0] == 0:
            bot.send_message(message.chat.id, messages[language]['name_prompt'])
            bot.register_next_step_handler(message, get_user_name, email)
        else:
            bot.send_message(message.chat.id, messages[language]['user_exists'])
            get_user_info(message)  # Запрашиваем email заново
        cursor.close()
        connection.close()
    else:
        bot.send_message(message.chat.id, messages[language]['invalid_email'])
        bot.register_next_step_handler(message, validate_email)

def get_user_name(message, email):
    global user_name
    user_name = message.text.strip()
    if not user_name:
        user_name = 'user'
    
    user_id = generate_unique_id()
    user_db_config = read_db_config('users_result.txt')
    connection = connect_to_database(user_db_config)
    cursor = connection.cursor()
    save_user_data_to_database(email, user_name, user_id, cursor, connection)
    cursor.close()
    connection.close()

    bot.send_message(message.chat.id, messages[language]['user_added'])
    show_main_menu(message)

def generate_unique_id():
    return str(uuid.uuid4())

def save_user_data_to_database(email, user_name, user_id, cursor, connection):
    try:
        query = "SELECT COUNT(*) FROM user_results WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result[0] == 0:
            query = "INSERT INTO user_results (email, user_name, user_id, first_usage_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (email, user_name, user_id, datetime.now()))
            connection.commit()
        else:
            print("Пользователь уже существует в базе данных.")
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(messages[language]['year'], messages[language]['duration'], messages[language]['rating'], 
               messages[language]['genre'], messages[language]['actor'], messages[language]['title'], 
               messages[language]['description'], messages[language]['language'], messages[language]['start_search'])
    bot.send_message(message.chat.id, messages[language]['parameter_choice'], reply_markup=markup)
    bot.register_next_step_handler(message, handle_main_menu)

def handle_main_menu(message):
    if message.text == messages[language]['year']:
        handle_year_menu(message)
    elif message.text == messages[language]['duration']:
        handle_duration_menu(message)
    elif message.text == messages[language]['rating']:
        handle_rating_menu(message)
    elif message.text == messages[language]['genre']:
        handle_genre_menu(message)
    elif message.text == messages[language]['actor']:
        handle_actor_menu(message)
    elif message.text == messages[language]['title']:
        handle_title_menu(message)
    elif message.text == messages[language]['description']:
        handle_description_menu(message)
    elif message.text == messages[language]['language']:
        handle_language_menu(message)
    elif message.text == messages[language]['start_search']:
        execute_movie_search(message)
    else:
        bot.send_message(message.chat.id, messages[language]['invalid_choice'])
        show_main_menu(message)

def handle_year_menu(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('1', '2', '3', '4')
    bot.send_message(message.chat.id, PROMPT_YEAR[language], reply_markup=markup)
    bot.register_next_step_handler(message, handle_year)

def handle_year(message):
    global search_params
    search_params['year'] = ['', '']
    year_comparison_choice = message.text.strip()
    if year_comparison_choice != '4':
        year_comparison = COMPARISON_OPTIONS[language].get(year_comparison_choice)
        search_params['year'][0] = year_comparison
        bot.send_message(message.chat.id, f"{messages[language]['year']} ({YEAR_RANGE[0]} to {YEAR_RANGE[1]}): ")
        bot.register_next_step_handler(message, handle_year_value)
    else:
        search_params['year'] = ['', '']
        show_main_menu(message)

def handle_year_value(message):
    year = message.text.strip()
    if not (year.isdigit() and int(year) in range(YEAR_RANGE[0], YEAR_RANGE[1] + 1)):
        bot.send_message(message.chat.id, f"Ошибка: {messages[language]['year']} ({YEAR_RANGE[0]} to {YEAR_RANGE[1]}).")
        bot.register_next_step_handler(message, handle_year_value)
        return
    search_params['year'][1] = year
    show_main_menu(message)

def handle_duration_menu(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('1', '2', '3', '4')
    bot.send_message(message.chat.id, PROMPT_DURATION[language], reply_markup=markup)
    bot.register_next_step_handler(message, handle_runtime)

def handle_runtime(message):
    global search_params
    search_params['runtime'] = ['', '']
    duration_comparison_choice = message.text.strip()
    if duration_comparison_choice != '4':
        duration_comparison = COMPARISON_OPTIONS[language].get(duration_comparison_choice)
        search_params['runtime'][0] = duration_comparison
        bot.send_message(message.chat.id, f"{messages[language]['duration']} ({DURATION_RANGE[0]} to {DURATION_RANGE[1]}): ")
        bot.register_next_step_handler(message, handle_runtime_value)
    else:
        search_params['runtime'] = ['', '']
        show_main_menu(message)

def handle_runtime_value(message):
    duration = message.text.strip()
    if not (duration.isdigit() and int(duration) in range(DURATION_RANGE[0], DURATION_RANGE[1] + 1)):
        bot.send_message(message.chat.id, f"Ошибка: {messages[language]['duration']} ({DURATION_RANGE[0]} to {DURATION_RANGE[1]}).")
        bot.register_next_step_handler(message, handle_runtime_value)
        return
    search_params['runtime'][1] = duration
    show_main_menu(message)

def handle_rating_menu(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('1', '2', '3', '4')
    bot.send_message(message.chat.id, PROMPT_RATING[language], reply_markup=markup)
    bot.register_next_step_handler(message, handle_rating)

def handle_rating(message):
    global search_params
    search_params['imdb_rating'] = ['', '']
    rating_comparison_choice = message.text.strip()
    if rating_comparison_choice != '4':
        rating_comparison = COMPARISON_OPTIONS[language].get(rating_comparison_choice)
        search_params['imdb_rating'][0] = rating_comparison
        bot.send_message(message.chat.id, f"{messages[language]['rating']} ({RATING_RANGE[0]} to {RATING_RANGE[1]}): ")
        bot.register_next_step_handler(message, handle_rating_value)
    else:
        search_params['imdb_rating'] = ['', '']
        show_main_menu(message)

def handle_rating_value(message):
    rating = message.text.strip()
    if not (rating.replace('.', '', 1).isdigit() and RATING_RANGE[0] <= float(rating) <= RATING_RANGE[1]):
        bot.send_message(message.chat.id, f"Ошибка: {messages[language]['rating']} ({RATING_RANGE[0]} to {RATING_RANGE[1]}).")
        bot.register_next_step_handler(message, handle_rating_value)
        return
    search_params['imdb_rating'][1] = rating
    show_main_menu(message)

def handle_genre_menu(message):
    bot.send_message(message.chat.id, PROMPT_GENRE[language])
    bot.register_next_step_handler(message, handle_genre)

def handle_genre(message):
    search_params['genre'] = message.text.strip()
    show_main_menu(message)

def handle_actor_menu(message):
    bot.send_message(message.chat.id, PROMPT_ACTOR[language])
    bot.register_next_step_handler(message, handle_actor)

def handle_actor(message):
    search_params['actor'] = message.text.strip()
    show_main_menu(message)

def handle_title_menu(message):
    bot.send_message(message.chat.id, PROMPT_TITLE[language])
    bot.register_next_step_handler(message, handle_title)

def handle_title(message):
    search_params['title'] = message.text.strip()
    show_main_menu(message)

def handle_description_menu(message):
    bot.send_message(message.chat.id, PROMPT_DESCRIPTION[language])
    bot.register_next_step_handler(message, handle_description)

def handle_description(message):
    search_params['description'] = message.text.strip()
    show_main_menu(message)

def handle_language_menu(message):
    bot.send_message(message.chat.id, PROMPT_LANGUAGE[language])
    bot.register_next_step_handler(message, handle_language)

def handle_language(message):
    search_params['language_input'] = message.text.strip()
    show_main_menu(message)

def execute_movie_search(message):
    global offset
    film_db_config = read_db_config('Database.txt')
    connection = connect_to_database(film_db_config)
    cursor = connection.cursor()

    query = "SELECT SQL_CALC_FOUND_ROWS title, year, genres, imdb_rating, poster, plot FROM movies WHERE 1=1"
    params = []

    if 'year' in search_params and search_params['year'][0]:
        query += f" AND year {search_params['year'][0]} %s"
        params.append(search_params['year'][1])
    if 'runtime' in search_params and search_params['runtime'][0]:
        query += f" AND runtime {search_params['runtime'][0]} %s"
        params.append(search_params['runtime'][1])
    if 'imdb_rating' in search_params and search_params['imdb_rating'][0]:
        query += f" AND imdb_rating {search_params['imdb_rating'][0]} %s"
        params.append(search_params['imdb_rating'][1])
    if 'genre' in search_params and search_params['genre']:
        genres = [g.strip() for g in search_params['genre'].split(',')]
        genre_conditions = " OR ".join("genres LIKE %s" for _ in genres)
        query += f" AND ({genre_conditions})"
        params.extend(f"%{g}%" for g in genres)
    if 'actor' in search_params and search_params['actor']:
        actors = [a.strip() for a in search_params['actor'].split(',')]
        actor_conditions = " OR ".join("cast LIKE %s" for _ in actors)
        query += f" AND ({actor_conditions})"
        params.extend(f"%{a}%" for a in actors)
    if 'title' in search_params and search_params['title'] and search_params['title'] != '4':
        query += " AND title LIKE %s"
        params.append(f"%{search_params['title']}%")
    if 'description' in search_params and search_params['description'] and search_params['description'] != '4':
        descriptions = [d.strip() for d in search_params['description'].split(',')]
        description_conditions = " OR ".join("plot LIKE %s" for _ in descriptions)
        query += f" AND ({description_conditions})"
        params.extend(f"%{d}%" for d in descriptions)
    if 'language_input' in search_params and search_params['language_input'] and search_params['language_input'] != '4':
        languages = [l.strip() for l in search_params['language_input'].split(',')]
        language_conditions = " OR ".join("languages LIKE %s" for _ in languages)
        query += f" AND ({language_conditions})"
        params.extend(f"%{l}%" for l in languages)

    if not params:
        query += " ORDER BY imdb_rating DESC LIMIT 10 OFFSET %s"
    else:
        query += " ORDER BY imdb_rating DESC LIMIT 10 OFFSET %s"
    params.append(offset)

    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.execute("SELECT FOUND_ROWS()")
        total_results = cursor.fetchone()[0]
        if results:
            bot.send_message(message.chat.id, RESULTS_HEADER[language].format(total_results))
            for i, row in enumerate(results, start=1):
                title = row[0]
                year = row[1]
                genres = row[2]
                rating = row[3]
                poster = row[4]
                plot = row[5]
                plot_translated = translate_text(plot, get_language_code(language))
                bot.send_message(message.chat.id, RESULTS_FORMAT[language].format(title, year, genres, rating))
                bot.send_message(message.chat.id, f"{RESULTS_POSTER[language].format(poster)}\n{plot_translated}")
        else:
            bot.send_message(message.chat.id, "Фильмы по заданным параметрам не найдены.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при выполнении запроса: {e}")

    # Update user search data after search execution
    search_details_dict = {
        'genre': search_params['genre'] if 'genre' in search_params and search_params['genre'] != '4' else '',
        'title': search_params['title'] if 'title' in search_params and search_params['title'] != '4' else '',
        'cast': search_params['actor'] if 'actor' in search_params and search_params['actor'] != '4' else '',
        'plot': search_params['description'] if 'description' in search_params and search_params['description'] != '4' else '',
    }

    user_db_config = read_db_config('users_result.txt')
    user_db_connection = connect_to_database(user_db_config)
    user_db_cursor = user_db_connection.cursor()
    update_user_search_data(email, search_details_dict, user_db_cursor, user_db_connection)
    user_db_cursor.close()
    user_db_connection.close()

    cursor.close()
    connection.close()

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('1', '2', '3')
    bot.send_message(message.chat.id, PROMPT_NEXT_ACTION[language], reply_markup=markup)
    bot.register_next_step_handler(message, next_action)

def update_user_search_data(email, search_details_dict, cursor, connection):
    try:
        cursor.execute("SELECT * FROM user_results WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            updated_fields = []
            updated_values = []
            
            if search_details_dict['genre']:
                updated_fields.append("lover_genres = IFNULL(CONCAT_WS(',', lover_genres, %s), %s)")
                updated_values.extend([search_details_dict['genre'], search_details_dict['genre']])
            if search_details_dict['title']:
                updated_fields.append("lover_title = IFNULL(CONCAT_WS(',', lover_title, %s), %s)")
                updated_values.extend([search_details_dict['title'], search_details_dict['title']])
            if search_details_dict['cast']:
                updated_fields.append("lover_cast = IFNULL(CONCAT_WS(',', lover_cast, %s), %s)")
                updated_values.extend([search_details_dict['cast'], search_details_dict['cast']])
            if search_details_dict['plot']:
                updated_fields.append("search_results = IFNULL(CONCAT_WS(',', search_results, %s), %s)")
                updated_values.extend([search_details_dict['plot'], search_details_dict['plot']])
            
            updated_fields.append("search_counter = search_counter + 1")
            updated_values.append(email)

            update_query = f"UPDATE user_results SET {', '.join(updated_fields)} WHERE email = %s"
            cursor.execute(update_query, updated_values)
            connection.commit()
            print("Данные пользователя успешно обновлены.")
        else:
            print("Пользователь не найден.")
    except Exception as e:
        print(f"Ошибка при обновлении данных пользователя: {e}")

def next_action(message):
    global offset
    next_action_choice = message.text.strip()
    if next_action_choice == '1':
        offset += 10
        execute_movie_search(message)
    elif next_action_choice == '2':
        offset = 0
        search_params.clear()
        show_main_menu(message)
    elif next_action_choice == '3':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('/start')
        bot.send_message(message.chat.id, messages[language]['search_complete'], reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('1', '2', '3')
        bot.send_message(message.chat.id, PROMPT_NEXT_ACTION[language], reply_markup=markup)
        bot.register_next_step_handler(message, next_action)

bot.polling(none_stop=True)
