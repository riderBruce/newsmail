import time
import asyncio
import aiohttp
import requests
import urllib3
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def search_daum_news(key_row):
    keyword = key_row[0]
    x_word = key_row[1]
    sTxt = keyword + ' ' + x_word

    columns = ['제목', 'URL', '언론사', 'KeyWord', '포털명']
    df = pd.DataFrame(columns=columns)

    # 다음 검색시 헤더가 삽입되면 로봇으로 간주함
    async with aiohttp.ClientSession() as session:
        for page in range(1, 50):
            now_ymdhms = datetime.now().strftime('%Y%m%d%H%M%S')  # Today
            day_ago_ymdhms = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d%H%M%S')  # D-1 날짜

            url = f"https://search.daum.net/search?w=news&cluster=n" \
                  f"&q={keyword}" \
                  f"&sort=recency&DA=STC&period=d" \
                  f"&sd={day_ago_ymdhms}" \
                  f"&ed={now_ymdhms}" \
                  f"&p={page}"
            async with session.get(url) as resp:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')
                il_Array = soup.select("ul.list_news li")

                for i in il_Array:
                    try:
                        try:
                            title = i.select_one("div.wrap_cont a").text
                        except:
                            title = None
                        try:
                            link = i.select_one("div.wrap_cont a").attrs["href"]
                        except:
                            link = None
                        try:
                            site = i.select_one("div > span.cont_info > a").text
                        except:
                            site = None
                        rNews = [title, link, site, keyword, "Daum"]
                        df = df.append(pd.Series(rNews, index=['제목', 'URL', '언론사', 'KeyWord', '포털명']), ignore_index=True)
                    except Exception as ex:
                        print(ex)

                # print(f" DAUM {keyword} {page} 검색중입니다...")

                isNext = soup.select_one("div.result_message.mg_cont.hide")
                if not isNext:
                    break


    print(f">> DAUM {keyword} 검색이 끝났습니다.")

    return df
