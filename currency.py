import asyncio
import platform
import sys
from datetime import datetime, timedelta
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


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

async def data_parser(days,currency):
    if days > 10 or days <=0:
        print(f"\nYOU SET BIG OR SMALL VALUE FOR DAYS\nTRY ENTER VALUE FROM 1 TO 10\n")
    if days == 1:
        currentDate = datetime.now().date()
        date2 = currentDate.strftime("%d.%m.%Y")
        await main(currency= currency,date = date2)

    elif days > 1:
        for i in range(0,days):
            delta = timedelta(days=i)
            currentDate = datetime.now().date() - delta
            date2 = currentDate.strftime("%d.%m.%Y")
            await  main(currency=currency,date = date2)


currency_completer = WordCompleter(['USD', 'AUD', 'AZN', 'BYN', "CAD", "CHF", "CNY", "CZK", "DKK", "EUR", "GBP", "ILS","JPY","KZT","MDL","NOK","PLN","SEK","SGD","TMT","TRY","UZS","XAU"])
days_completer = [i for i in range(0,11)]

if __name__== "__main__":
    # curr = sys.argv[1]
    if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print("Push SPACE in input to see all currencies ID!")
    CURRENCY_INPUT = prompt('Enter currency: ', completer=currency_completer)
    DAYS_INPUT = prompt("Enter days: ",completer=days_completer)
    a = asyncio.run(data_parser(DAYS_INPUT,CURRENCY_INPUT))
