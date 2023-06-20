import platform
from datetime import date, timedelta
import aiohttp
import asyncio
import sys

max_days = 10

async def main():
    n = len(sys.argv)
    if n < 2:
        return "number of days is required"
    try:
        ndays = int(sys.argv[1])
    except:
        return "number of days must be a number"
    if ndays > 10:
        return "maximum number of days is 10"

    day = date.today()
    result = []

    async with aiohttp.ClientSession() as session:
        for i in range(ndays):
            sday = day.strftime("%d.%m.%Y")
            async with session.get('https://api.privatbank.ua/p24api/exchange_rates?json&date='+sday) as response:
            
                rate = await response.json()
                rate = rate["exchangeRate"]
                eur = rate[1]
                usd = rate[6]
                rate_dict = {"EUR":{"sale":eur["saleRateNB"],"purchase":eur["purchaseRateNB"]},
                            "USD":{"sale":usd["saleRateNB"],"purchase":usd["purchaseRateNB"]}}
                result.append({sday:rate_dict})
            day -= timedelta(days=1)
    return result


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)