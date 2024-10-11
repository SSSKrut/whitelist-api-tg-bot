import yaml
import logging

try:
    with open(".config.yml", "r") as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            logging.error("Error reading the config file")
            print(exc)
except FileNotFoundError:
    logging.error("Config file not found")

# Read the token from the file
BOT_TOKEN = config["telegram_token"]

ADMIN_ID = config["admins"]

WHITELIST_URL = config["whitelist_url"]
