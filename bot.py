import telebot
from config import token
from db import insert_row
from validators import is_stt_block_limit
from speechkit import speech_to_text
from db import create_table
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    create_table()
    bot.send_message(message.chat.id, "Добро пожаловать в бота, который транскрибирует аудио!Нажми на /stt")

@bot.message_handler(commands=['stt'])
def stt_handler(message):
    user_id = message.from_user.id
    bot.send_message(
        chat_id=user_id,
        text="Отправь голосовое сообщение🔊, чтобы я его распознал!💬"
    )
    bot.register_next_step_handler(message, stt)
def stt(message):
    user_id = message.from_user.id

    # Проверка, что сообщение действительно голосовое
    if not message.voice:
        bot.send_message(
            chat_id=user_id,
            text="Пожалуйста, запиши ГС"
        )
        bot.register_next_step_handler(message, stt)
        return

    # Считаем аудиоблоки и проверяем сумму потраченных аудиоблоков
    stt_blocks, error = is_stt_block_limit(message, message.voice.duration)
    if not stt_blocks:
        bot.send_message(user_id, 'Слишком длинное аудио')
        return

    file_id = message.voice.file_id  # получаем id голосового сообщения
    file_info = bot.get_file(file_id)  # получаем информацию о голосовом сообщении
    file = bot.download_file(file_info.file_path)  # скачиваем голосовое сообщение

    # Получаем статус и содержимое ответа от SpeechKit
    status, text = speech_to_text(file)  # преобразовываем голосовое сообщение в текст

    # Если статус True - отправляем текст сообщения и сохраняем в БД, иначе - сообщение об ошибке
    if status:
        # Записываем сообщение и кол-во аудиоблоков в БД
        insert_row(user_id, text, 'stt_blocks', stt_blocks)
        bot.send_message(
            chat_id=user_id,
            text=text,
            reply_to_message_id=message.id
        )
    else:
        bot.send_message(user_id, text)
bot.polling()