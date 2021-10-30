from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, Filters, MessageHandler

from Database import add
state_1 = 1
state_2 = 2


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Universitet id sini yuboring", reply_markup=ReplyKeyboardRemove())
    return state_1


def command_1(update, context):
    univer = update.message.text
    if univer.isdigit():
        update.message.reply_text("Fakultitet idlarini yuboring\n"
                                  "Masalan 1, 2,3 4, 5, 6")
        context.user_data['univer'] = int(univer)
        return state_2
    else:
        update.message.reply_text("Qayta kiriting xato buldi")
        return state_1


def command_2(update, context):
    facs = update.message.text
    datas = facs.split(',')
    univer = context.user_data['univer']
    for i in datas:
        if i.isdigit():
            add(univer, int(i))
            update.message.reply_text(univer, int(i))
    update.message.reply_text("Muaffaqiyatli qo'shildi yana universitet id sini yuboring:")
    return state_1


updater = Updater('1784595918:AAEwdvkX58FvNmXuIFTqdecMsMA0VFPJgys')

conv_hand = ConversationHandler(
    entry_points=[
        CommandHandler('hello', hello)
    ],
    states={
        state_1: [
            MessageHandler(Filters.text, command_1)
        ],
        state_2: [
            MessageHandler(Filters.text, command_2)
        ]
    },
    fallbacks=[CommandHandler('hello', hello)]
)
updater.dispatcher.add_handler(conv_hand)

updater.start_polling()
updater.idle()
