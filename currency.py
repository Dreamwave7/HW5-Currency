from datetime import datetime
import asyncio
import aiohttp
import sys
import platform



async def main(currency:str, date:datetime = None):
    async with aiohttp.ClientSession() as connect:
        async with connect.get(f"https://api.privatbank.ua/p24api/exchange_rates?json&date=20.04.2023") as response:
            result = await response.json()
            await currency_parser(result, currency = currency)


async def currency_parser(jsonfile:dict, currency:str, date = None):
     for currencies in jsonfile["exchangeRate"]:
         if currencies["currency"] == currency.upper():
            print(f"Валюта : {currencies['currency']}\nКурс продажу НБУ: {currencies['saleRateNB']}\nКурс продажу ПриватБанку: {currencies['saleRate']}\nКурс купівлі ПриватБанку :{currencies['purchaseRate']}")


if __name__== "__main__":
    if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    r = asyncio.run(main("PLN"))
