
# 패키지 상대경로
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from typing import Iterator

import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE


from get_naver_news import search_naver_news
from get_daum_news import search_daum_news
from get_google_news import search_google_news
from correct_data import *
from check_each_pages import *
from get_final_news import *
from config import SEARCH_KEY_ROWS, GOOGLE_KEYS
from additional_func import time_checker


@time_checker
def collect_daily_news() -> pd.DataFrame:
    tasks = []
    tasks += [search_naver_news(key_row) for key_row in SEARCH_KEY_ROWS]
    tasks += [search_daum_news(key_row) for key_row in SEARCH_KEY_ROWS]
    tasks += [search_google_news(key_row) for key_row in GOOGLE_KEYS]
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    task_results = asyncio.run(asyncio.wait(tasks))

    dfs = [res.result() for res in list(task_results[0])]
    df = pd.concat(dfs)
    print(df.shape)

    return df


@time_checker
def correct_data(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_special_character(df)
    df = put_http_in_front_of_address(df)
    df = check_blacklist_media(df)
    df = check_major_media(df)
    df = check_exception_word_in_title(df)
    df = sort_data_by_priority(df)
    df = check_identical_article(df)
    df = sort_data_by_identical(df)
    df = check_similar_title(df)
    df = sort_data_by_similarity(df)
    return df


@time_checker
def check_pages(df: pd.DataFrame) -> pd.DataFrame:
    urls = list(dict.fromkeys(df['URL'].tolist()))
    df_pages = get_each_pages_simultaneously(urls)
    df = pd.merge(df, df_pages, how='left', on='URL')
    df = check_exception_word_in_page(df)
    df = sort_data_after_check_inside(df)

    return df


def arrange_final_news(df: pd.DataFrame) -> pd.DataFrame:
    df = get_final_news(df)
    save_data(df, result_file_name)
    df = get_mailing_data(df)
    return df


if __name__ == '__main__':
    df = collect_daily_news()
    df = correct_data(df)
    df = check_pages(df)
    df = arrange_final_news(df)

    result_file_name = r"d:\result_with_each_page.xlsx"
    df.to_excel(result_file_name)

