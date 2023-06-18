from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ChatPermissions

from database import BotBD

from config.config import *
from keyboards import *

BotBD = BotBD()

bot = Bot(token=tg_token)
dp = Dispatcher(bot)

img = ''


@dp.message_handler(content_types=['text'])
async def check_user(message: types.Message):
    print(message.chat.id)
    if message.chat.id == chat:
        exist = BotBD.user_exists(user_id=message.from_user.id)
        if not exist:
            await message.delete()
            await bot.send_message(chat_id=message.chat.id, text="Click here to prove you`re human",
                                   reply_markup=inject_prove)
            await bot.restrict_chat_member(chat, message.from_user.id, ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False))
        else:
            await bot.restrict_chat_member(chat, message.from_user.id, ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True))
            await filter(message)


@dp.message_handler(content_types=['text'])
async def filter(message: types.Message):
    if int(message.chat.id) == int(chat):
        chat_admin2 = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if ("http" or "https") in message.text:
            print(chat_admin2)
            if str(chat_admin2["status"]) != ('creator' or 'admin'):
                await message.delete()
            else:
                await check_user(message)


@dp.message_handler(content_types=['new_chat_members'])
async def send(message: types.Message):
    if int(message.chat.id) == int(chat):
        try:
            name = message.from_user.username

            if name is None:
                name = str(message.from_user.first_name)

            await bot.send_photo(message.chat.id, img, caption=f"Hello @{name}. \nWelcome to the channel <b>Test</b> 🎮",
                                 parse_mode=types.ParseMode.HTML, reply_markup=inject_buttons)

        except Exception:
            name = "@" + message.from_user.username
            fname = message.from_user.username

            if fname is None:
                name = str(message.from_user.first_name)

            await bot.send_photo(message.chat.id, img, caption=f"Hello @{name}. \nWelcome to the channel <b>Test</b> 🎮",
                                 parse_mode=types.ParseMode.HTML, reply_markup=inject_buttons)


@dp.callback_query_handler(text='confirm')
async def add_user(message: types.CallbackQuery):
    try:
        exist = BotBD.user_exists(user_id=message.from_user.id)

        if not exist:
            BotBD.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, text='You has successfully registered')
            await bot.restrict_chat_member(chat, message.from_user.id, ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True))
        else:
            await bot.restrict_chat_member(chat, message.from_user.id, ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True))


    except Exception:
        pass

executor.start_polling(dp, skip_updates=True)
