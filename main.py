import os
import telebot
import speech_recognition
from pydub import AudioSegment
from telebot import TeleBot

bot: TeleBot = telebot.TeleBot('6882568785:AAHBw7yRGNTa_7COC5xT4nrYbfepvfJwD_A')


def oga2wav(filename):
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename


def recognize_speech(oga_filename):
    wav_filename = oga2wav(oga_filename)
    recognizer = speech_recognition.Recognizer()

    with speech_recognition.AudioFile(wav_filename) as source:
        wav_audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(wav_audio, language='en')
    except speech_recognition.UnknownValueError:
        text = "Unable to recognize speech"
    except speech_recognition.RequestError:
        text = "Recognition request failed"

    if os.path.exists(oga_filename):
        os.remove(oga_filename)

    if os.path.exists(wav_filename):
        os.remove(wav_filename)

    return text


def download_file(bot, file_id):
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = file_id + file_info.file_path
    filename = filename.replace('/', '_')
    with open(filename, 'wb') as f:
        f.write(downloaded_file)
    return filename


@bot.message_handler(commands=['start'])
def greeting(message):
    greet_text = f'Hello, {message.from_user.first_name}! How can I help you?'
    bot.send_message(message.chat.id, greet_text)


@bot.message_handler(content_types=['voice'])
def transcript(message):
    filename = download_file(bot, message.voice.file_id)
    text = recognize_speech(filename)
    bot.send_message(message.chat.id, text)


bot.polling()
