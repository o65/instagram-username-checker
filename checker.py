import asyncio
import aiohttp
from typing import List
from os import system
from itertools import cycle

def open_file() -> List[str]:
    with open('usernames.txt', 'r', encoding='UTF-8') as f:
        file_contents = [line.strip('\n') for line in f]

    return file_contents

def write_file(arg: str) -> None:
    with open('available.txt', 'a', encoding='UTF-8') as f:
        f.write(f'{arg}\n')

class Checker:
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
    def __init__(self, usernames: List[str]):
        self.to_check = usernames


    async def _check(self, session: aiohttp.ClientSession, username: str) -> None:     
        async with session.get('https://www.instagram.com/%s' % username) as response:
            try:
                r = await response.text()

                if response.status == 404:
                    print('%s[+] https://www.instagram.com/%s%s' % ('\u001b[32;1m', username, '\u001b[0m'))
                    write_file(username)

                elif response.status == 200 and 'Login • Instagram' in r:
                    print('[~] Ratelimited, unable to check', username)
                else:
                    print('%s[-] https://www.instagram.com/%s%s' % ('\u001b[31;1m', username, '\u001b[0m'))

            except Exception as e:
                print('[ERROR] ' + e)                    
                    
    async def start(self):
        tasks = []
        async with aiohttp.ClientSession(headers=self.HEADERS) as session:
            for i in self.to_check:
                tasks.append(asyncio.create_task(self._check(session, i)))
            system('cls')
            input("Press enter to begin..")
            task = await asyncio.gather(*tasks)
            return task

if __name__ == '__main__':
    system('title [Instagram Checker]')
    system('cls')
    username_list = open_file() 
    checker = Checker(username_list)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(checker.start())