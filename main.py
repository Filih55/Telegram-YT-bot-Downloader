import os
import logging
import telegram
import pytube

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram API token
TOKEN = '<5686417198:AAEA1kzPsXGmNFIcjZOyo5JAQaiR_xaygjw>'
bot = telegram.Bot(token=TOKEN)

# Define a function to handle incoming messages
def download_video(update, context):
    # Get the chat ID and message text
    chat_id = update.message.chat_id
    message_text = update.message.text

    # Try to parse the message and get the video URL and resolution
    try:
        video_url, resolution = message_text.split(' ')
    except ValueError:
        bot.send_message(chat_id=chat_id, text='Please enter a valid YouTube video URL and resolution (e.g. https://www.youtube.com/watch?v=video_id 720p).')
        return

    # Try to download the video
    try:
        # Create a PyTube object for the video URL
        video = pytube.YouTube(video_url)

        # Get the stream with the specified resolution
        stream = video.streams.filter(res=f'{resolution}p').first()

        # Set up the output file path
        file_path = os.path.join(os.getcwd(), f'{video.title}.mp4')

        # Download the video
        stream.download(output_path=os.getcwd(), filename=video.title)

        # Send the video file to the user
        with open(file_path, 'rb') as f:
            bot.send_video(chat_id=chat_id, video=f)

        # Delete the video file from the server
        os.remove(file_path)

    # Handle errors
    except Exception as e:
        logger.error(f'Error downloading video: {e}')
        bot.send_message(chat_id=chat_id, text='Error downloading video.')

# Set up the Telegram bot
updater = telegram.ext.Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Register the download_video function to handle incoming messages
dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text & (~telegram.ext.Filters.command), download_video))

# Start the bot
updater.start_polling()
updater.idle()
