import platform
import sys
from datetime import datetime, timedelta

import aiohttp
import asyncio

url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
currency = ['USD', 'EUR']


async def date_parse(days: int) -> list:
    date = datetime.now()
    dates = (date - timedelta(days=x) for x in range(days))
    dates = list(map(lambda x: x.strftime('%d.%m.%Y'), dates))
    return dates


async def show_info(info: dict):
    informs = []
    for inf in info['exchangeRate']:
        inform = {}
        if inf['currency'] in currency:
            inform['currence'] = inf['currency']
            inform['sale'] = inf['saleRate']
            inform['purcase'] = inf['purchaseRate']
            informs.append(inform)
    return informs


async def main(days: int):
    results = {}
    async with aiohttp.ClientSession() as session:
        date_list = await date_parse(days)
        for date in date_list:
            try:
                async with session.get(f'{url}{date}') as response:
                    if response.status == 200:
                        result = await response.json()
                        result = await show_info(result)
                        results[date] = result
                    else:
                        print(f"Error status: {response.status} for {url}")
            except aiohttp.ClientConnectorError as err:
                print(f'Connection error: {url}', str(err))
    return results


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        monit_days = int(sys.argv[1])
        if monit_days not in range(1, 11):
            print('Моніторинг здійсьнюється за термін від 1 до 10 днів')
            monit_days = 1
    except IndexError:
        monit_days = 1
    res = asyncio.run(main(monit_days))
    for key in res:
        print(key)
        for n in res[key]:
            print(n)