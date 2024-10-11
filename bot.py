from aiogram import Bot, Dispatcher, types
from aiogram.filters import BaseFilter
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
import logging
import asyncio
import requests
import json

from config import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


logging.info("Current admin list: %s", ADMIN_ID)
logging.info("Current whitelist url: %s", WHITELIST_URL)


class IsRegistered(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in ADMIN_ID


@dp.message(Command("add"), IsRegistered())
async def add_message(message: types.Message):
    domain = message.text[len("/add ") :].strip()
    if domain is None or domain == "":
        await message.reply(f"Domain?")
        return

    params = {"domain": f"{domain}"}
    command = "allow_domain"
    response = requests.get(f"{WHITELIST_URL}/{command}", json=params)
    logging.info(f"Sending request to {response.url}")

    if response.status_code == 200:
        await message.reply(f"{domain} добавлен")
    else:
        error_message = f"{response.status_code}: {response.text}"
        logging.error(error_message)
        await message.reply(error_message)


@dp.message(Command("addip"), IsRegistered())
async def addip_message(message: types.Message):
    ip = message.text[len("/addip ") :].strip()
    if ip is None or ip == "":
        await message.reply(f"Ip?")
        return

    params = {"ip": f"{ip}"}
    command = "add_ip"
    response = requests.get(f"{WHITELIST_URL}/{command}", json=params)
    logging.info(f"Sending request to {response.url}")

    if response.status_code == 200:
        await message.reply(f"{ip} добавлен")
    else:
        error_message = f"{response.status_code}: {response.text}"
        logging.error(error_message)
        await message.reply(error_message)


@dp.message(Command("get"), IsRegistered())
async def get_message(message: types.Message):
    params = {}
    command = "get_list"
    response = requests.get(f"{WHITELIST_URL}/{command}", json=params)
    logging.info(f"Sending request to {response.url}")

    if response.status_code == 200:
        json_data = json.dumps(response.json(), indent=2)
        ips_file = types.BufferedInputFile(
            json_data.encode("utf-8"), filename="whitelist.json"
        )
        await message.answer_document(ips_file)
    else:
        error_message = f"{response.status_code}: {response.text}"
        logging.error(error_message)
        await message.reply(error_message)


# Filter for any not-command messages from registered users
@dp.message(IsRegistered())
async def privileged_user_message(message: types.Message):
    logging.info(f"{message.from_user.id}: {message.text}")


# Filter for any not-command messages from unregistered users
@dp.message()
async def unprivileged_user_message(message: types.Message):
    logging.info(f"{message}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
