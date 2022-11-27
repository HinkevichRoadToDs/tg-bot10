import telegram
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    Filters
)
from logger import log

updater = Updater('5895651223:AAF6T83aKexUHwF7Tes--lLi2j1-RdzxjCA')


def choise_action(update: Update, context: CallbackContext):
    global result
    log(update,context)
    result.append(update.message.text)

    buttonSum = telegram.KeyboardButton(text='plus')
    buttonSubtr = telegram.KeyboardButton(text='minus')
    buttonMult = telegram.KeyboardButton(text='multiply')
    buttonDiv = telegram.KeyboardButton(text='divide')
    buttonEqual = telegram.KeyboardButton(text='result')
    buttonCancel = telegram.KeyboardButton(text='cancel')

    button_list =[[buttonSum,buttonSubtr,buttonMult,buttonDiv,buttonEqual,buttonCancel]]
    reply_markup = telegram.ReplyKeyboardMarkup(button_list, one_time_keyboard=True,resize_keyboard=True)
    update.message.reply_text(f'Текущее выражение : {"".join(result)}\nВыберите операцию:',reply_markup=reply_markup)


def cancel_all(update: Update, context: CallbackContext):
    global result
    log(update, context)
    result = []
    update.message.reply_text(f'Выражение очищено, введите первое число:')

def greeting_command(update: Update, context: CallbackContext):
    global result
    result = []
    log(update, context)
    update.message.reply_text(f'{update.effective_user.first_name},'
                              f'вы на главной.')
    update.message.reply_text(f'Введите первое число:')
    # choise_action

def operator_plus(update: Update, context: CallbackContext):
    global result
    log(update, context)
    result.append('+')
    update.message.reply_text(f'Текущее выражение : {"".join(result)}')
    update.message.reply_text(f'Введите число: ')


def operator_minus(update: Update, context: CallbackContext):
    global result
    log(update, context)
    result.append('-')
    update.message.reply_text(f'Текущее выражение : {"".join(result)}')
    update.message.reply_text(f'Введите число: ')


def operator_multiply(update: Update, context: CallbackContext):
    global result
    log(update, context)
    result.append('*')
    update.message.reply_text(f'Текущее выражение : {"".join(result)}')
    update.message.reply_text(f'Введите число: ')


def operator_divide(update: Update, context: CallbackContext):
    global result
    log(update, context)
    result.append('/')
    update.message.reply_text(f'Текущее выражение : {"".join(result)}')
    update.message.reply_text(f'Введите число: ')

def simple_math(sample):
    if sample[1] == '+':
         return [sample[0] + sample[2]]
    if sample[1] == '-':
        return [sample[0] - sample[2]]
    if sample[1] == '*':
        return [sample[0] * sample[2]]
    if sample[1] == '/':
        return [sample[0] / sample[2]]

def conversion(item):
    global result
    if 'j' in item:
        return complex(item)
    else:
        try:
            return float(item)
        except:
            return item

def find_result(update: Update, context: CallbackContext):
    global result
    log(update, context)
    temp = result.copy()
    # try:
    result = list(map(conversion,result))
    print(result)
    # except:
    #     update.message.reply_text('Incorrect entering some of the elements. Try again')
    #     result = []
    try:
        while len(result) != 1:
            for sign in '/*+-':
                while sign in result:
                    idx = result.index(sign)
                    result = result[:idx - 1] + simple_math(result[idx - 1:idx + 2]) + result[idx + 2:]
    except:
        update.message.reply_text('Incorrect entering some of the elements. Try again')
        result = []
    print(result)
    update.message.reply_text(f'{"".join(temp)}={result[len(result) - 1]}')
    result = []
    update.message.reply_text(f'{update.effective_user.first_name},'
                             f'вы на главной.')
    update.message.reply_text(f'Введите первое число:')

updater.dispatcher.add_handler(CommandHandler('start', greeting_command))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('plus'), operator_plus))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('minus'), operator_minus))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('multiply'), operator_multiply))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('divide'), operator_divide))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('result'), find_result))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('cancel'), cancel_all))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(''), choise_action))

# поиск обновлений
updater.start_polling()
print('engine started')
# Останавка бота, если были нажаты Ctrl + C
updater.idle()