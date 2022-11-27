from telegram import Update
from telegram.ext import Updater, CallbackContext


def log(update: Update, context: CallbackContext):
    with open('log.csv', 'a') as fl:
        fl.write(f'{update.effective_user.first_name},{update.effective_user.id},{update.message.text}\n')