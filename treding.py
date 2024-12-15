from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time
import threading

# In-memory database to store user IDs and admin messages
users = set()
admin_message = None
is_waiting = False

# Replace with your channel's invite link
CHANNEL_LINK = "https://t.me/your_channel"

# Function to send periodic "I am alive" messages
def send_alive_messages(context: CallbackContext):
    while is_waiting:
        for user_id in users:
            context.bot.send_message(chat_id=user_id, text="I am alive. Please wait.")
        time.sleep(60)  # Wait for 1 minute

# Command: /start
def start(update: Update, context: CallbackContext):
    global admin_message, is_waiting
    user_id = update.effective_user.id
    user_status = context.bot.get_chat_member(chat_id='@your_channel', user_id=user_id).status

    if user_status in ["member", "administrator", "creator"]:
        users.add(user_id)
        update.message.reply_text("Welcome! You will receive updates from the admin here.")
        if not is_waiting:
          is_waiting = True
          threading.Thread(target=send_alive_messages, args=(context,), daemon=True).start()
    else:
        update.message.reply_text(f"Please join our channel first to receive updates: {CHANNEL_LINK}")

# Command: /send <message>
def send(update: Update, context: CallbackContext):
    global admin_message, is_waiting
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("You are not authorized to use this command.")
        return

    admin_message = ' '.join(context.args)
    for user_id in users:
        context.bot.send_message(chat_id=user_id, text=f"Admin Message: {admin_message}")

    if not is_waiting:
        is_waiting = True
        threading.Thread(target=send_alive_messages, args=(context,), daemon=True).start()

# Command: /end
def end(update: Update, context: CallbackContext):
    global is_waiting
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("You are not authorized to use this command.")
        return

    if is_waiting:
        is_waiting = False
        for user_id in users:
            context.bot.send_message(chat_id=user_id, text="Waiting period has ended.")
    else:
        update.message.reply_text("No waiting message is active.")

# Main function
def main():
    global ADMIN_ID

    # Replace 'YOUR_BOT_TOKEN' with your bot token
    TOKEN = '7819122771:AAF53JU3qlrZ0CEaeZvQQH2mQlMUA65j7sI'

    # Replace with your Telegram user ID
    ADMIN_ID = "itsnishant470"

    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("send", send, pass_args=True))
    dp.add_handler(CommandHandler("end", end))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
