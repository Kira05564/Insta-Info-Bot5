#!/usr/bin/env python
# Author: Alienkrishn [Anon4You]
import telebot
import instaloader
import requests
import os

with open('token.txt', 'r') as file:
    bot_token = file.read().strip()

bot = telebot.TeleBot(bot_token)
loader = instaloader.Instaloader()

print("Your bot has started!")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me an Instagram username for info.")

@bot.message_handler(func=lambda message: True)
def send_instagram_info(message):
    username = message.text.strip()
    loading_message = bot.reply_to(message, "Fetching profile info...")

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        info = (
            f"👤 *Username:* {profile.username}\n"
            f"📅 *Full Name:* {profile.full_name}\n"
            f"📝 *Bio:* {profile.biography}\n"
            f"🌍 *Website:* {profile.external_url}\n"
            f"📸 *Posts:* {profile.mediacount}\n"
            f"🔔 *Followers:* {profile.followers}\n"
            f"🔗 *Following:* {profile.followees}\n"
            f"🆔 *Instagram ID:* {profile.userid}\n"
            f"📘 *Facebook Mention ID:* {profile.fb_id if hasattr(profile, 'fb_id') else 'N/A'}\n"
            f"👥 *Private Account:* {'Yes' if profile.is_private else 'No'}\n"
            f"\n✨ *Created by* [Alienkrishn](https://github.com/Anon4You)"
        )

        profile_pic_url = profile.profile_pic_url
        profile_pic_response = requests.get(profile_pic_url)
        profile_pic_path = f"{username}_profile_pic.jpg"

        with open(profile_pic_path, 'wb') as photo_file:
            photo_file.write(profile_pic_response.content)

        with open(profile_pic_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=info, parse_mode='Markdown')

        os.remove(profile_pic_path)

    except Exception as e:
        bot.reply_to(message, f"Error fetching data for {username}. Error: {str(e)}")

    bot.delete_message(chat_id=loading_message.chat.id, message_id=loading_message.message_id)

if __name__ == '__main__':
    bot.polling()
