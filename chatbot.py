from telegram import Update, ParseMode, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, RegexHandler
import configparser
import os
import logging
import redis
global redis1
from Database import Database
from Paper import Paper
import requests
from io import BytesIO


# TODO: Add total downloaded times [redis]

def main():
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    global redis1
    redis1 = redis.Redis(host=(os.environ['HOST']),
                         password=(os.environ['PASSWORD']),
                         port=(os.environ['REDISPORT']))

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level = logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("hello", hello))
    dispatcher.add_handler(CommandHandler("searchSchool", searchSchool))
    dispatcher.add_handler(CommandHandler("searchPaper", searchPaper))
    dispatcher.add_handler(RegexHandler(r'^/sp(\w+)$', searchPaperRegex))
    dispatcher.add_handler(RegexHandler(r'^/file(\w+)$', fileIDRegex))

    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        replyText = ""
        for key in redis1.scan_iter('*'):
            value = redis1.get(key)
            replyText += f"({key.decode('UTF-8')}: {value.decode('UTF-8')}
        update.message.reply_text(replyText)
        # logging.info(context.args[0])
        # msg = context.args[0]  # /add keyword <-- this should store the keyword
        # redis1.incr(msg)
        # update.message.reply_text('You have said ' + msg + ' for ' +
        #                           redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')


def hello(update: Update, context: CallbackContext) -> None:
    try:
        logging.info(context.args[0])
        name = context.args[0]
        update.message.reply_text(f"Good day, {name}!")

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')


# TODO: /help command to list all static commands
def help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')


# Enable /searchSchool command to obtain {schoolCode} by searching {schoolName}
def searchSchool(update: Update, context: CallbackContext) -> None:
    from School import School
    try:
        logging.info(context.args[0])
        searchString = context.args[0]
        db = Database()
        records = db.searchSchool(searchString)

        count = len(records)
        schools = [School(*kwargs) for kwargs in records]

        if count == 0:
            update.message.reply_text(f"We cannot found any 🏫 for your request. Try again.",
                                  reply_to_message_id=update.message.message_id)
            return

        replyText = f"Good news! We found {count} 🏫 for your request!\n"

        for school in schools:
            replyText += f"""<b>🏫[/sp{school.code}] {school.chinesename}</b>
<i>{school.englishname}</i>
\n"""

        update.message.reply_text(replyText,
                                  reply_to_message_id=update.message.message_id,
                                  parse_mode=ParseMode.HTML)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')


# Allow /searchPaper command from {schoolCode, form, exam/test, fileType, year) to [fileDescription, fileType, fileSize]
def __sp(update: Update, context: CallbackContext, searchString) -> None:
    db = Database()
    records = db.searchPaper(searchString)

    count = len(records)
    papers = [Paper(*kwargs) for kwargs in records]

    if count == 0:
        update.message.reply_text(f"We cannot found any 📄 for your request. Try again.",
                                  reply_to_message_id=update.message.message_id)
        return

    else:
        replyText = f"Good news! We found {count} 📄 for your request!\n"

        for paper in papers:
            replyText += f"""<strong>{paper.name}</strong>
📄/file{paper.fileID} ({paper.fileType}, {paper.human_readable_size})
\n"""

        update.message.reply_text(replyText,
                                  reply_to_message_id=update.message.message_id,
                                  parse_mode=ParseMode.HTML)


def searchPaperRegex(update: Update, context: CallbackContext) -> None:
    try:
        logging.info(context.matches[0].group(1))
        __sp(update, context, searchString=context.matches[0].group(1))

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>',
                                  reply_to_message_id=update.message.message_id)


def searchPaper(update: Update, context: CallbackContext) -> None:
    try:
        logging.info(context.args[0])
        __sp(update, context, searchString=context.args[0])

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>',
                                  reply_to_message_id=update.message.message_id)


# Allow dynamic /file<id> command to download file hosted on GDrive
# TODO: Downloaded times [redis]
def fileIDRegex(update: Update, context: CallbackContext) -> None:
    try:
        logging.info(context.matches[0].group(1))
        file_id = context.matches[0].group(1)
        db = Database()
        args = db.getFileID(file_id)

        paper = Paper(*args)

        # file = InputFile.from_url(file_url)
        response = requests.get(paper.gdrivelink, allow_redirects=True)
        file = InputFile(BytesIO(response.content), filename=paper.name)

        # Send the file as an attachment
        context.bot.send_document(chat_id=update.effective_chat.id, document=file)

        redis1.incr(paper.name)

    except (IndexError, ValueError):
        update.message.reply_text(f'Cannot find fileId {context.matches[0].group(1)}',
                                  reply_to_message_id=update.message.message_id)


if __name__ == '__main__':
    main()