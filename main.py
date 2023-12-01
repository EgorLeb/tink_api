import datetime
import time

from tinkoff.invest import Client, CandleInterval, Quotation

TOKEN = "TOKEN"


def get_rub(m: Quotation):
    return m.units + m.nano / 1000000000


ans = []
tot = 0
start = time.time()
with Client(TOKEN) as client:
    for i in client.instruments.shares().instruments:
        try:
            if i.currency == "rub" and len(client.instruments.get_dividends(figi=i.figi).dividends) > 0:
                print(i.figi, i.ticker, i.currency, i.name)
                # input()
                if time.time() - start > 15:
                    time.sleep(70)
                    start = time.time()
                for j in client.instruments.get_dividends(figi=i.figi).dividends:
                    if j.close_price.currency == "rub":
                        try:
                            # datetime.datetime(2022, 7, 1, 0, 0, tzinfo=datetime.timezone.utc)
                            start_day = j.last_buy_date
                            finish_day = start_day + datetime.timedelta(days=7)
                            price = get_rub(j.dividend_net)
                            # print(start_day)
                            # print(finish_day)
                            # print(price)
                            day_of_close = []
                            day_after_div = []
                            for pp in client.market_data.get_candles(figi=i.figi, from_=start_day, to=start_day + datetime.timedelta(days=1),
                                                                     interval=CandleInterval.CANDLE_INTERVAL_HOUR).candles:
                                day_of_close.append([pp.time - start_day, get_rub(pp.low)])
                            for pp in client.market_data.get_candles(figi=i.figi, from_=start_day + datetime.timedelta(days=1), to=finish_day,
                                                                     interval=CandleInterval.CANDLE_INTERVAL_HOUR).candles:
                                day_after_div.append([pp.time - start_day, get_rub(pp.low)])
                                # print(pp.time)
                                # print(get_rub(pp.close))
                            if len(day_after_div) != 0 and len(day_of_close) != 0 and price > 0 and 0.007 < day_of_close[-1][1] / price:
                                total_list = day_of_close[-1:] + day_after_div
                                # print(day_of_close)
                                # print(day_after_div)
                                ans += [[(total_list[i][1] - total_list[1 + i][1]) / price for i in range(len(total_list) - 1)]]
                                tot += 1
                                res = []
                                cn = 0
                                for iii in range(20):
                                    s = 0
                                    for jjj in range(tot):
                                        if len(ans[jjj]) > iii:
                                            cn += 1
                                            s += ans[jjj][iii]
                                    s /= cn
                                    res.append(s)
                                print(res)
                                # print(total_list)
                                # print(ans, tot, sum(ans) / tot)
                                # print()
                                # print(j, price, "\n\n\n")
                                # print(client.market_data.get_candles(figi=i.figi, from=, interval=CandleInterval.CANDLE_INTERVAL_5_MIN))
                        except BaseException as e:
                            print(e)
                            raise
                        finally:
                            e = 2
        except BaseException as e:
            print(e)
            raise
        finally:
            e = 2
# print(ans)
# print(tot)
# print(sum(ans) / tot)
