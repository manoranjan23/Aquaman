import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from pytube import YouTube

API_ID = '27884171'  # Apna API ID yahan daalein
API_HASH = 'abe760b5d6b33e15c676577d6ae4a06a'  # Apna API Hash yahan daalein
BOT_TOKEN = '7313059877:AAGiCX8wPk-F6G00xoDeoNR-dQZ4HIRS1I0'  # Apna Bot Token yahan daalein
ASSISTANT_ID = '6851334207'  # Apna Assistant ID yahan daalein

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to handle start command
@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Welcome to the Music Bot! Use /play <song_name> to start playing.")

# Function to handle when the bot is added to a group
@app.on_chat_member_updated()
async def handle_chat_member_updated(client, chat_member_updated: ChatMemberUpdated):
    if chat_member_updated.new_chat_member.status in ['member', 'administrator']:
        await client.send_message(
            chat_id=chat_member_updated.chat.id,
            text="Thank you for adding me to the group! Use /play <song_name> to start playing music."
        )

# Function to play music from YouTube
@app.on_message(filters.command("play"))
async def play_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a song name to play. Usage: /play <song_name>")
        return
    
    song_name = message.text.split(" ", 1)[1]
    await message.reply_text(f"Loading {song_name}...")
    
    try:
        # Download song from YouTube
        yt = YouTube(f"https://www.youtube.com/results?search_query={song_name}")
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(filename="song.mp4")
        
        # Send song details
        await client.send_audio(
            chat_id=message.chat.id,
            audio="song.mp4",
            title=yt.title,
            performer=yt.author,
            thumb=yt.thumbnail_url
        )

        # Clean up
        os.remove("song.mp4")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

# Function to pause the music
@app.on_message(filters.command("pause"))
async def pause_command(client, message):
    await message.reply_text("Music paused.")

# Function to resume the music
@app.on_message(filters.command("resume"))
async def resume_command(client, message):
    await message.reply_text("Music resumed.")

# Function to stop the music
@app.on_message(filters.command("stop"))
async def stop_command(client, message):
    await message.reply_text("Music stopped.")

# Function to skip the music
@app.on_message(filters.command("skip"))
async def skip_command(client, message):
    await message.reply_text("Music skipped.")

app.run()