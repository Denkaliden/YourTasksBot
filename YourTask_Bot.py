import telebot
import time
import threading
#Ну это токен
token = 'Токен'
bot = telebot.TeleBot(token)
user_tasks = {}
#Команда старт, тоже самое что и хелп.
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для управления задачами. Используй /help чтобы ознакомиться с инструментарием.")
#Выводит все команды и пояснения к ним
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "*/add ваш_текст* - Добавляет задачу в список\n\n*/remove номер_задачи* - убирает задачу по номеру из списка\n\n*/list* - Показывает все ваши задачи и их номера\n\n*/clear* - очищает весь список разом\n\n*/edit номер_задачи новый_текст* - Позволяет изменить текст одной из задач\n\n*/set_timer номер_задачи время_в_минутах* - установка таймера на задачу, чтобы бот напомнил вам о ней через время")
#Получение нового списка для нового пользователя
def get_user_tasks(user_id):
    if user_id not in user_tasks:
        user_tasks[user_id] = []
    return user_tasks[user_id]
#Добавление задачи в персональный user_list
@bot.message_handler(commands=['add'])
def add_task(message):
    user_id = message.from_user.id
    task = message.text[len('/add '):]
    tasks = get_user_tasks(user_id)
    if task:
        tasks.append(task)
        bot.reply_to(message, f'Задача добавлена: "{task}"')
    else:
        bot.reply_to(message, 'Пожалуйста, введите задачу.')
#Убрать задачу из списка(По номеру задачи, а не по названию)
@bot.message_handler(commands=['remove'])
def remove_task(message):
    user_id = message.from_user.id
    tasks = get_user_tasks(user_id)
    try:
        task_id = int(message.text[len('/remove '):]) - 1
        if 0 <= task_id < len(tasks):
            removed_task = tasks.pop(task_id)
            bot.reply_to(message, f'Задача удалена: "{removed_task}"')
        else:
            bot.reply_to(message, 'Неверный номер задачи.')
    except (ValueError, IndexError):
        bot.reply_to(message, 'Пожалуйста, укажите номер задачи для удаления.')
#Вывести список задач с номерами
@bot.message_handler(commands=['list'])
def list_tasks(message):
    user_id = message.from_user.id
    tasks = get_user_tasks(user_id)
    if tasks:
        tasks_list = '\n'.join([f"{i + 1}. {task}" for i, task in enumerate(tasks)])
        bot.reply_to(message, f'Ваши задачи:\n{tasks_list}')
    else:
        bot.reply_to(message, 'Список задач пуст.')
#Очистить весь список разом
@bot.message_handler(commands=['clear'])
def clear_tasks(message):
    user_id = message.from_user.id
    tasks = get_user_tasks(user_id)
    tasks.clear()
    bot.reply_to(message, 'Все задачи удалены.')
#Редактирование одной задачи из списка
@bot.message_handler(commands=['edit'])
def edit_task(message):
    user_id = message.from_user.id
    tasks = get_user_tasks(user_id)
    try:
        task_info = message.text[len('/edit '):].split(" ", 1)
        task_id = int(task_info[0]) - 1
        new_task_text = task_info[1]

        if 0 <= task_id < len(tasks):
            old_task = tasks[task_id]
            tasks[task_id] = new_task_text
            bot.reply_to(message, f'Задача изменена: "{old_task}" на "{new_task_text}"')
        else:
            bot.reply_to(message, 'Неверный номер задачи.')
    except (ValueError, IndexError):
        bot.reply_to(message, 'Используйте команду в формате: */edit номер_задачи новый_текст*')
#Это для таймера
def notify_task(user_id, task):
    bot.send_message(user_id, f'Время заняться задачей "{task}"')
#Установка таймера на задачу, только в минутах((
@bot.message_handler(commands=['set_timer'])
def set_timer(message):
    user_id = message.from_user.id
    tasks = get_user_tasks(user_id)
    try:
        timer_info = message.text[len('/set_timer '):].split(" ", 1)
        task_id = int(timer_info[0]) - 1
        timer_minutes = int(timer_info[1])
        if 0 <= task_id < len(tasks):
            task = tasks[task_id]
            bot.reply_to(message, f'Таймер на задачу "{task}" установлен на {timer_minutes} минут.')
            def timer_thread(task):
                time.sleep(timer_minutes * 60)
                notify_task(message.chat.id, task)
            threading.Thread(target=timer_thread, args=(task,)).start()
        else:
            bot.reply_to(message, 'Неверный номер задачи.')
    except (ValueError, IndexError):
        bot.reply_to(message, 'Используйте команду в формате:*/set_timer номер_задачи время_в_минутах*')
#Душа бота
@bot.message_handler(commands=['easter_egg'])
def easter_egg(message):
    pashalka = '''
⠀⠀⠀⡶⢶⡴⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣧⠀⠁⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⣀⣀⠀⠀⠀
⠀⢠⠟⠉⣠⣄⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣯⠙⠁⣸⠇⠀⠀
⢠⡎⢀⡼⠋⠈⢋⣁⣀⣀⠀⠀⠀⠀⣀⠤⠶⠶⠶⢤⡀⢸⣇⡴⢦⡈⠙⢦⠀
⣾⠁⣾⣁⣴⡾⢛⣉⠭⠭⢽⣲⣶⣋⣁⣠⣴⣶⡶⠶⠟⠶⠶⢦⡀⠙⣦⠘⣆
⡏⠀⣿⣿⡿⠗⠉⠁⠀⣀⡠⢬⣍⣉⣛⡻⠟⢉⡤⢖⡤⣭⣍⠐⠻⣆⢸⠀⢸
⡇⠀⣿⣿⠁⠀⢀⡴⢋⡕⢫⢚⡿⢶⡄⠈⡿⠉⠁⣼⡟⣧⣽⣇⢀⡞⣾⠀⢸
⡇⠀⣿⣿⠀⠋⠱⣞⡁⠀⢹⣯⣻⣾⣿⠴⠓⠤⠤⠼⠛⠛⠉⣭⢯⡀⡟⠀⢸
⡇⠀⢸⣿⠀⡠⠶⠶⠾⠿⠾⢭⣉⣁⣤⣤⣤⡤⠤⠴⠶⠒⣉⣀⡼⢱⠇⠀⢸
⡇⠀⠸⣿⠘⠧⣀⣘⡒⠲⠶⠦⠤⠤⠤⠤⠴⠶⠶⠖⠒⢋⣉⣴⣣⠞⠀⢀⡞
⢷⠀⠀⢿⣆⡀⠀⠉⠉⠉⠑⠲⠶⠶⠶⠶⠶⠒⠒⠛⠋⠉⢉⣉⣼⡀⢀⡴⠟
⠘⣧⠀⠈⠻⣿⣷⣦⣤⣄⣀⣀⣠⣤⣤⣤⣤⣤⣤⣶⣿⣿⣿⣿⣿⣟⠁⠀⠀
⠀⢸⣷⣄⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀
⠀⠚⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠋⠀⠀
    '''
    bot.reply_to(message, pashalka)
@bot.message_handler(func=lambda message: True)
def handle_unrecognized_message(message):
    bot.reply_to(message, "Пожалуйста, используйте /help для получения списка команд.")
bot.polling()
