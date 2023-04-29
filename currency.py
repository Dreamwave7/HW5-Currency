import asyncio
import platform
import sys
from datetime import datetime

import aiohttp

separator = "========================================"

async def main(currency:str, date:datetime):
    async with aiohttp.ClientSession() as connect:
        async with connect.get(f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}") as response:
            result = await response.json()
            await currency_parser(result, currency = currency, date=date)


async def currency_parser(jsonfile:dict, currency:str, date):
     for currencies in jsonfile["exchangeRate"]:
         if currencies["currency"] == currency.upper():
            print(separator)
            print(f"Поточна дата : {date}\nБазова валюта : {currencies['baseCurrency']}\nВалюта : {currencies['currency']}\nКурс продажу НБУ : {currencies['saleRateNB']}\nКурс продажу ПриватБанку : {currencies['saleRate']}\nКурс купівлі ПриватБанку : {currencies['purchaseRate']}")
            print(separator)

async def data_parser(days,currency="usd"):
    currentDate = datetime.now().date()
    date2 = currentDate.strftime("%d.%m.%Y")
    await main(currency= currency,date = date2)

if __name__== "__main__":
    # curr = sys.argv[1]
    if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # r = asyncio.run(main(curr))
    a = asyncio.run(data_parser(2))
