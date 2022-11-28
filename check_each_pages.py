import aiohttp
import asyncio
import time
import re
from typing import Tuple, Union
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
# xlwt -> openpyxl 설치하여야 엑셀로 파일 저장 가능
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

from config import EXCEPTION_KEY_LEVEL_0, EXCEPTION_KEY_LEVEL_1, EXCEPTION_KEY_LEVEL_2
from additional_func import time_checker

m = 0


def get_each_pages_simultaneously(urls: list) -> pd.DataFrame:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    coroutines = (control_session(url) for url in urls)
    task_results = asyncio.run(limit_with_semaphore(coroutines))

    dfs = [res.result() for res in list(task_results[0])]
    df = pd.concat(dfs)

    return df


async def control_session(url: str) -> pd.DataFrame:
    columns = ['URL', 'TEXT']
    df = pd.DataFrame(columns=columns)

    headers = {'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 "
                             "Edge/18.19582"
               }
    connector = aiohttp.TCPConnector(limit=50)
    total_timeout = aiohttp.ClientTimeout(total=1, sock_connect=50)
    # timeout을 길게해주면 전체 실행 후 미완료된 딜레이로 에러 발생 추측됨
    async with aiohttp.ClientSession(headers=headers, connector=connector, timeout=total_timeout) as session:
        body_text = await get_text(session, url)
        row = [url, body_text]
        df = df.append(pd.Series(data=row, index=columns), ignore_index=True)
        # global m
        # m += 1
        # print(f"{m} 개가 실행 완료되었습니다.....")

    return df


async def limit_with_semaphore(coroutines):
    semaphore = asyncio.Semaphore(50)

    async def sem_coro(coro):
        async with semaphore:
            if semaphore.locked():
                print(f"> > > now limit controlling, {semaphore._waiters.__len__()} is waiting....")
            return await coro

    tasks = [asyncio.ensure_future(sem_coro(coroutine)) for coroutine in coroutines]
    return await asyncio.wait(tasks)


async def get_text(session, url):
    try:
        async with session.get(url) as resp:
            html = await resp.content.read()
            http_encoding = resp.charset if 'charset' in resp.headers.get('content-type', '').lower() else None
            html_encoding = EncodingDetector.find_declared_encoding(html, is_html=True)
            encoding = html_encoding or http_encoding
            soup = BeautifulSoup(html.decode(encoding, 'replace'), 'html.parser')
            try:
                body_text = soup.select_one('body')
                body_text = (body_text.get_text()
                             .replace('\n', ' ')
                             .replace('\r', ' ')
                             .replace('\t', ' ')
                             .replace('\'', ' '))
                body_text = ILLEGAL_CHARACTERS_RE.sub(r'', body_text)
            except Exception as ex:
                body_text = ex
    except Exception as ex:
        body_text = ex

    return body_text


def check_exception_word_in_page(df: pd.DataFrame) -> pd.DataFrame:

    def is_contain_exception_word(row: pd.Series) -> Tuple[Union[str, bool], bool]:
        content = row['TEXT']
        keyword = row['KeyWord']
        contain_words = ''
        is_dropped = False

        def has_exception_key_by_level(content: str, EXCEPTION_KEYS: list, limit_of_exception: int) -> str:
            text = ''
            for key in EXCEPTION_KEYS:
                try:
                    num_of_exception_key = content.count(key)
                except:
                    num_of_exception_key = 0
                if num_of_exception_key:
                    text += f"{key}({num_of_exception_key}) / "
                if num_of_exception_key >= limit_of_exception:
                    nonlocal is_dropped
                    is_dropped = True
            return text

        contain_words += 'Lv1 : ' + has_exception_key_by_level(content, EXCEPTION_KEY_LEVEL_1, 1)
        contain_words += 'Lv2 : ' + has_exception_key_by_level(content, EXCEPTION_KEY_LEVEL_2, 5)

        def has_important_word(keyword: str):
            text = ''
            important_words = ['안전 사고', '지배구조']
            for important_word in important_words:
                if important_word in keyword:
                    text += f"Lv3 : {important_word} ★ "
                    nonlocal is_dropped
                    is_dropped = False
            return text

        contain_words += has_important_word(keyword)

        if contain_words == '':
            contain_words = False

        return contain_words, is_dropped

    df[['text_contained', 'text_drop']] = df.apply(is_contain_exception_word, axis=1, result_type='expand')
    return df



def sort_data_after_check_inside(df: pd.DataFrame) -> pd.DataFrame:
    effective_columns = ['제목', 'URL', '언론사', 'KeyWord', '포털명',
                         'key_drop', 'is_title_same', '언론사_is_black', 'similarity',
                         'TEXT', 'text_contained', 'text_drop', '언론사_not_major']
    df = df[effective_columns]
    df = df.sort_values(by=['key_drop', 'is_title_same', '언론사_is_black', 'similarity', 'text_drop', '언론사_not_major',
                            '제목'], kind='mergesort')
    df = df.reset_index(drop=True)
    return df


if __name__ == '__main__':
    # 앞단에서 도출된 데이터 사용
    data_file = r"d:\result_with_each_page.xlsx"
    df = pd.read_excel(data_file)


    @time_checker
    def check_pages(df: pd.DataFrame) -> pd.DataFrame:
        # urls = list(dict.fromkeys(df['URL'].tolist()))
        # df_pages = get_each_pages_simultaneously(urls)
        # df = pd.merge(df, df_pages, how='left', on='URL')
        df = check_exception_word_in_page(df)
        df = sort_data_after_check_inside(df)
        return df

    df = check_pages(df)
    result_file = r"d:\result_with_each_page1.xlsx"
    df.to_excel(result_file)









# def get_each_pages_simultaneously(urls: list) -> pd.DataFrame:
#     # loop = asyncio.get_event_loop()
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     # task_results = loop.run_until_complete(task_controller(urls))
#     # loop.close()
#     task_results = asyncio.run(task_controller(urls))
#
#     dfs = [res.result() for res in list(task_results[0])]
#     df = pd.concat(dfs)
#
#     return df
#
#
# async def task_controller(urls: list):
#     limit = asyncio.Semaphore(50)
#     tasks = [asyncio.ensure_future(get_each_page(url, limit)) for url in urls]
#
#     return await asyncio.wait(tasks)
#
#
# async def get_each_page(url: str, limit) -> pd.DataFrame:
#     async with limit:
#         if limit.locked():
#             global n
#             n += 1
#             print(f"{n} : now limit controlling, wait....")
#             # await asyncio.sleep(0.5)
#
#         columns = ['URL', 'TEXT']
#         df = pd.DataFrame(columns=columns)
#
#         headers = {'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 "
#                                  "Edge/18.19582"
#                    }
#         connector = aiohttp.TCPConnector(limit=60)
#         async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
#             try:
#                 async with session.get(url) as resp:
#                     html = await resp.content.read()
#                     http_encoding = resp.charset if 'charset' in resp.headers.get('content-type', '').lower() else None
#                     html_encoding = EncodingDetector.find_declared_encoding(html, is_html=True)
#                     encoding = html_encoding or http_encoding
#                     soup = BeautifulSoup(html.decode(encoding, 'replace'), 'html.parser')
#                     try:
#                         body_text = soup.select_one('body')
#                         body_text = (body_text.get_text()
#                                      .replace('\n', ' ')
#                                      .replace('\r', ' ')
#                                      .replace('\t', ' ')
#                                      .replace('\'', ' '))
#                         body_text = ILLEGAL_CHARACTERS_RE.sub(r'', body_text)
#                     except Exception as ex:
#                         body_text = ex
#             except Exception as ex:
#                 # print(url, ex)
#                 body_text = ex
#             row = [url, body_text]
#             df = df.append(pd.Series(data=row, index=columns), ignore_index=True)
#             global m
#             m += 1
#             print(f"{m} 개가 실행 되었습니다.....")
#
#     return df
#
#
# def check():
#     for eli in EXCEPTION_KEY_LEVEL_1:
#         count1 = str(eachBodyText).count(eli)
#         if count1 >= 1:
#             NewsRow[5] = f"2차 제외 : {eli}"
#             continue
#
#     if NewsRow[5] == "회피어없음":
#         for eli2 in EXCEPTION_KEY_LEVEL_2:
#             count2 = str(eachBodyText).count(eli2)
#             if count2 >= 5:
#                 if str(eachBodyText).count("지배구조") < 1:
#                     NewsRow[5] = f"3차 제외 : {eli2}"
#                     continue
