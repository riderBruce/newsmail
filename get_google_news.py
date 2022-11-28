import time
import asyncio
import aiohttp
import requests
import urllib3
from urllib import parse
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import pandas as pd
from GoogleNews import GoogleNews

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def search_google_news(key_row):
    columns = ['제목', 'URL', '언론사', 'KeyWord', '포털명']
    df = pd.DataFrame(columns=columns)

    keyword = parse.quote(key_row)

    headers = {'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/70.0.3538.102 "
                             "Safari/537.36 "
                             "Edge/18.19582 "}
    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"https://news.google.com/search?" \
              f"q='{keyword}'+" \
              f"when:1d"
        async with session.get(url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, 'html.parser')

            articles = soup.select('div[class="NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc"]')
            for article in articles:
                try:
                    # title
                    try:
                        title = article.find('h3').text
                    except:
                        title = None
                    # link
                    try:
                        link = 'news.google.com/' + article.find("h3").find("a").get("href")
                    except:
                        link = None
                    # site
                    try:
                        site = article.find("time").parent.find("a").text
                    except:
                        site = None
                except Exception as e_article:
                    print(e_article)

                rNews = [title, link, site, key_row, "Google"]
                df = df.append(pd.Series(rNews, index=['제목', 'URL', '언론사', 'KeyWord', '포털명']), ignore_index=True)

            # print(f" Google {keyword} 검색중입니다...")

    print(f">> Google {keyword} 검색이 끝났습니다.")

    return df
