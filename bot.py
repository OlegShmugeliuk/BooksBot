from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler


PAYMENT_STATE = 1


def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [KeyboardButton('ua'), KeyboardButton('ru'), KeyboardButton('en')]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    update.message.reply_text('Виберіть мову / Choose your language:', reply_markup=reply_markup)


def echo(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text

    if message_text.lower() == 'ua':
        update.message.reply_text('Виберіть спосіб оплати / Choose payment method:', reply_markup=get_payment_keyboard())
        return PAYMENT_STATE
    elif message_text.lower() == 'en':
        update.message.reply_text('Choose payment method:', reply_markup=get_payment_keyboard())
        return PAYMENT_STATE


def handle_payment_choice(update: Update, context: CallbackContext) -> None:
    choice = update.message.text
    if choice.lower() == 'карта' or choice.lower() == 'card':
        update.message.reply_text('Ви вибрали оплату карткою / You have chosen card payment. Перекажіть гроші на номер картки / Transfer money to card number: +1234567890')
        update.message.reply_text('Натисніть "Готово" коли оплата виконана / Press "Done" when the payment is completed', reply_markup=get_ready_button())
    elif choice.lower() == 'криптовалюта' or choice.lower() == 'cryptocurrency':
        update.message.reply_text('Ви вибрали оплату криптовалютою / You have chosen cryptocurrency payment. Відправте гроші на адресу / Send money to address: 0x71C7656EC7ab88b098defB751B7401B5f6d8976F')
        update.message.reply_text('Натисніть "Готово" коли оплата виконана / Press "Done" when the payment is completed', reply_markup=get_ready_button())


def handle_ready_button(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.username  
    context.bot.send_message(chat_id=-1001685108205, text=f'User {user_id} clicked "Готово" / "Done".')


def get_payment_keyboard():
    keyboard = [
        [KeyboardButton('Карта / Card'), KeyboardButton('Криптовалюта / Cryptocurrency')]
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)


def get_ready_button():
    keyboard = [[KeyboardButton('Готово / Done')]]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

if __name__ == '__main__':
    updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text & ~Filters.command, echo)],
        states={
            PAYMENT_STATE: [MessageHandler(Filters.text & ~Filters.command, handle_payment_choice)]
        },
        fallbacks=[],
    )

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.text(['Готово', 'Done']), handle_ready_button))

    updater.start_polling()
    updater.idle()

