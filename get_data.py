import aiohttp 
import asyncio
import os
import json
from dotenv import load_dotenv
from support_func import insert_date
from pprint import pprint

load_dotenv()
date = insert_date()


async def get_orders(
        date_from: str, key: str, flag: int = 1 
        ):
    url = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/orders' 
    params = {
                'dateFrom': date_from,
                'key': key,
                'flag': flag,
            }
    async with aiohttp.ClientSession() as session:
        flag = False
        count_request = 0
        while flag == False and count_request <= 10:
            try:
                async with session.get(url=url, params=params) as resp:
                    print(resp.status)
                    if resp.status == 200:
                        flag = True
                        orders = await resp.json()
                        with open('orders.json', 'w', encoding='utf-8') as file:
                            json.dump(orders, file, indent=4)
                    else:
                        count_request += 1
                    print(count_request)
            except Exception as E:
                print(f'Ecxeption in request for get orders: {E}')


async def get_report(
        date_from: str, date_to: str, key: str, limit: int = 1000, 
        rrdid: int = 0  
        ):
    url = 'https://suppliers-stats.wildberries.ru/api/v1/supplier/reportDetailByPeriod' 
    params = {
                'dateTo': date_to,
                'dateFrom': date_from,
                'key': key,
                'limit': limit,
                'rrdid': rrdid
            }
    async with aiohttp.ClientSession() as session:
        flag = False
        count_request = 0
        while flag == False and count_request <= 10:
            try:
                async with session.get(url=url, params=params) as resp:
                    print(resp.status)
                    if resp.status == 200:
                        flag = True
                        report = await resp.json()
                        if report is not None:
                            return report
                        else:
                            print(f'Response is null')
                            return  'Break' 
                    else:
                        count_request += 1
                    print(count_request)
            except Exception as E:
                print(f'Ecxeption in request for get orders: {E}')
        return None


async def main():
    try:
        count_rrdid = 0
        input_count = 0
        while True:
            answer_req = await get_report(
                '2022-09-25', date['date_to'], api_key, rrdid=count_rrdid
                )
            if answer_req == 'Break' or input_count >= 10:
                break
            elif answer_req is None:
                print(f'Count input = {input_count}')
                input_count += 1
            else:
                input_count = 0
                if not os.path.isfile('reports.json'):
                    with open('reports.json', 'w', encoding='utf-8') as file:
                        json.dump(answer_req, file, indent=4)
                    print('File reports.json create') 
                else:
                    with open('reports.json', 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        data = [*data, *answer_req]
                        print(f'Len data {len(data)}')
                        with open('reports.json', 'w', encoding='utf-8') as file:
                            json.dump(data, file, indent=4)
                count_rrdid += 1
    except Exception as E:
        print(f'Error in main func {E}')


if __name__ == '__main__':
    api_key = os.environ['APIKEY']
    asyncio.get_event_loop().run_until_complete(main())
