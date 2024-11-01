import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytube import YouTube
import ffmpeg

API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
BOT_TOKEN = 'YOUR_BOT_TOKEN'
ASSISTANT_ID = 'YOUR_ASSISTANT_ID'

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to handle start command
@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Welcome to the Music Bot! Use /play <song_name> to start playing.")

# Function to play music from YouTube
@app.on_message(filters.command("play"))
async def play_command(client, message):
    song_name = message.text.split(" ", 1)[1]
    await message.reply_text(f"Loading {song_name}...")
    
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