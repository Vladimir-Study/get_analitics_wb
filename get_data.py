import aiohttp 
import asyncio
import os
import json
import csv
from time import sleep
from dotenv import load_dotenv
from support_func import insert_date
from pprint import pprint

load_dotenv()
date = insert_date()


async def get_orders(
        date_from: str, key: str, flag: int = 0 
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
                    try:
                        if resp.status == 200:
                            flag = True
                            orders = await resp.json()
                            with open('orders.csv', 'w', encoding='1251') as file:
                                print('Writing to the file has started!')
                                headers = [
                                        "gNumber", "date", "lastChangeDate", "supplierArticle",
                                        "techSize", "barcode", "totalPrice", "discountPercent",
                                        "warehouseName", "oblast", "incomeID", "odid",
                                        "nmId", "subject", "category", "brand", "isCancel", 
                                        "sticker"
                                        ]
                                write_file = csv.DictWriter(file, delimiter=';',
                                        fieldnames = headers, lineterminator='\r',
                                        extrasaction='ignore')
                                write_file.writeheader()
                                for order in orders:
                                    write_file.writerow(order)
                            print('Writing to the file has been closed')
                    except aiohttp.client_exceptions.ClientPayloadError as E:
                        print(E)
                        sleep(3)
                    else:
                        count_request += 1
                        sleep(3)
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
                    try:
                        if resp.status == 200:
                            flag = True
                            report = await resp.json()
                            if report is not None:
                                return report
                            else:
                                print(f'Response is null')
                                return  'Break' 
                    except aiohttp.client_exceptions.ClientPayloadError as E:
                        print(E)
                        sleep(3)
                    else:
                        sleep(3)
                        count_request += 1
                    print(count_request)
            except Exception as E:
                print(f'Ecxeption in request for get reports: {E}')
        return None


async def main():
    api_key = os.environ['APIKEY']
    await get_orders(date['date_from'], api_key)
    try:
        count_rrdid = 0
        input_count = 0
        while True:
            reports = await get_report(
                date['date_from'], date['date_to'], api_key, rrdid=count_rrdid
                )
            if reports == 'Break' or input_count >= 10:
                break
            elif reports is None:
                print(f'Count input = {input_count}')
                input_count += 1
            else:
                input_count = 0
                if not os.path.isfile('reports.csv'):
                    with open('reports.csv', 'w', encoding='1251') as file:
                        print('Writing to the file has started!')
                        headers = [
                                    "realizationreport_id", "suppliercontract_code", "rid",
                                    "rr_dt", "rrd_id", "gi_id", "subject_name", "nm_id",
                                    "brand_name", "sa_name", "ts_name", "barcode", "doc_type_name",
                                    "quantity", "retail_price", "retail_amount", "sale_percent",
                                    "commission_percent", "office_name", "supplier_oper_name",
                                    "order_dt", "sale_dt", "shk_id", "retail_price_withdisc_rub",
                                    "delivery_amount", "return_amount", "delivery_rub",
                                    "gi_box_type_name", "product_discount_for_report", "supplier_promo",
                                    "ppvz_spp_prc", "ppvz_kvw_prc_base", "ppvz_kvw_prc", 
                                    "ppvz_sales_commission", "ppvz_for_pay", "ppvz_reward", 
                                    "ppvz_vw", "ppvz_vw_nds", "ppvz_office_id", "ppvz_office_name",
                                    "ppvz_supplier_id", "ppvz_supplier_name", "ppvz_inn", "declaration_number",
                                    "sticker_id", "site_country"
                                    ]
                        #json.dump(answer_req, file, indent=4)
                        write_file = csv.DictWriter(file, delimiter=';',
                                fieldnames = headers, lineterminator='\r',
                                extrasaction='ignore')
                        write_file.writeheader()
                        for report in reports:
                            write_file.writerow(report)
                    print('Writing to the file has been closed')
                    print('File reports.csv create') 
                else:
                    with open('reports.csv', 'a', encoding='1251') as file:
                        print('Writing to the file has continue!')
                        headers = [
                                    "realizationreport_id", "suppliercontract_code", "rid",
                                    "rr_dt", "rrd_id", "gi_id", "subject_name", "nm_id",
                                    "brand_name", "sa_name", "ts_name", "barcode", "doc_type_name",
                                    "quantity", "retail_price", "retail_amount", "sale_percent",
                                    "commission_percent", "office_name", "supplier_oper_name",
                                    "order_dt", "sale_dt", "shk_id", "retail_price_withdisc_rub",
                                    "delivery_amount", "return_amount", "delivery_rub",
                                    "gi_box_type_name", "product_discount_for_report", "supplier_promo",
                                    "ppvz_spp_prc", "ppvz_kvw_prc_base", "ppvz_kvw_prc", 
                                    "ppvz_sales_commission", "ppvz_for_pay", "ppvz_reward", 
                                    "ppvz_vw", "ppvz_vw_nds", "ppvz_office_id", "ppvz_office_name",
                                    "ppvz_supplier_id", "ppvz_supplier_name", "ppvz_inn", "declaration_number",
                                    "sticker_id", "site_country"
                                    ]
                        #json.dump(answer_req, file, indent=4)
                        write_file = csv.DictWriter(file, delimiter=';',
                                fieldnames = headers, lineterminator='\r',
                                extrasaction='ignore')
                        for report in reports:
                            write_file.writerow(report)
                        '''
                        data = json.load(file)
                        data = [*data, *answer_req]
                        print(f'Len data {len(data)}')
                        with open('reports.json', 'w', encoding='utf-8') as file:
                            json.dump(data, file, indent=4)
                        '''
                    print('Writing to the file has been closed')
                count_rrdid += 1
    except Exception as E:
        print(f'Error in main func {E}')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
