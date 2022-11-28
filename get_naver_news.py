import time
import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import pandas as pd


async def search_naver_news(key_row):

    keyword = key_row[0]
    x_word = key_row[1]
    sTxt = keyword + ' ' + x_word

    columns = ['제목', 'URL', '언론사', 'KeyWord', '포털명']
    df = pd.DataFrame(columns=columns)

    headers = {'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/70.0.3538.102 "
                             "Safari/537.36 "
                             "Edge/18.19582 "}
    async with aiohttp.ClientSession(headers=headers) as session:
        # where=news : 뉴스 섹션
        # sort=1 : 최신순 , sort=0 : 관련도순
        # pd=4 : 1일
        # field=1 : 제목만, field=0 : 전체
        sQuery = "http://search.naver.com/search.naver?where=news&sort=0&pd=4&field=0&query="+sTxt
        try:
            async with session.get(sQuery) as resp:
                # req = requests.get(sQuery, verify=False, timeout=30)
                # html = req.text
                # soup = BeautifulSoup(html,'html.parser')
                html = await resp.text()
                soup = BeautifulSoup(html,'html.parser')

                nPage = 1
                curPage = 0

                ul_Paging = soup.find('div',{'class','sc_page_inner'})
                if ul_Paging is None :
                    nPage = 1
                else :
                    aPaging = ul_Paging.find_all('a')
                    for il_page in aPaging :
                        nPage = nPage + 1

                while nPage > curPage :
                    # await asyncio.sleep(0.5)
                    startRow = 10 * curPage + 1
                    sQuery = "http://search.naver.com/search.naver?where=news&sort=0&pd=4&field=0&start=" + str(startRow) + "&query=" + sTxt
                    async with session.get(sQuery) as resp:
                        html = await resp.text()
                        soup = BeautifulSoup(html,'html.parser')

                        ul_body = soup.find('ul',{'class','list_news'})
                        if ul_body is None :
                            # logWrite('[네이버 검색결과] : ' + keyword + ' 해당 검색어에 해당하는 뉴스가 없습니다.')
                            break

                        il_Array = ul_body.find_all('li')

                        for il_row in il_Array:
                            try:
                                news = il_row.find('a',{'class','news_tit'})
                                if news is None : continue
                                source = il_row.find('a',{'class','info press'})
                                if source is None : continue
                                rNews = [news['title'],news['href'],source.get_text(),sTxt,"Naver"]
                                df = df.append(pd.Series(rNews, index=['제목', 'URL', '언론사', 'KeyWord', '포털명']), ignore_index=True)
                            except Exception as ex:
                                print(Exception)

                        ul_Paging = soup.find('div',{'class','sc_page'})
                        if ul_Paging is None :
                            break
                        isNext = ul_Paging.find('a',{'class','btn_next'})
                        if isNext is None :
                            break

                        curPage = curPage + 1

                        # print(f" NAVER {keyword} {curPage} 검색중입니다...")
        except Exception as ex:
            print("네이버검색 에러 :", ex)
    print(f">> NAVER {keyword} 검색이 끝났습니다.")

    return df