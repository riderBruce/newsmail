import re

import pandas as pd
from sentence_transformers import SentenceTransformer, util

from config import EXCEPTION_KEYS_ALL, BLACK_LIST_MEDIAS, MAJOR_MEDIAS, EXCEPTION_KEY_LEVEL_1, EXCEPTION_KEY_LEVEL_2


def remove_special_character(df: pd.DataFrame) -> pd.DataFrame:
    df['제목'] = df['제목'].apply(lambda x: re.sub('[^a-zA-Z0-9가-힣 \n\.]', ' ', x))
    df['제목'] = df['제목'].apply(lambda x: " ".join(x.split()).strip())
    return df


def put_http_in_front_of_address(df: pd.DataFrame) -> pd.DataFrame:
    df['URL'] = df['URL'].apply(lambda x: 'https://' + str(x) if not x.startswith('http') else str(x))
    return df


def check_blacklist_media(df: pd.DataFrame) -> pd.DataFrame:
    def is_blacklist_media(media: str) -> bool:
        return media in BLACK_LIST_MEDIAS

    def is_sport_media(media: str) -> bool:
        return "스포츠" in media

    df['언론사_is_black'] = df['언론사'].apply(is_blacklist_media or is_sport_media)
    return df


def check_major_media(df: pd.DataFrame) -> pd.DataFrame:
    def is_not_major_media(media: str) -> int:
        return media not in MAJOR_MEDIAS

    df['언론사_not_major'] = df['언론사'].apply(is_not_major_media)
    return df


def check_exception_word_in_title(df: pd.DataFrame) -> pd.DataFrame:
    def is_contain_exception_word(title: str) -> str:
        contain_words = ''
        for key in EXCEPTION_KEYS_ALL:
            if key in title:
                contain_words += key + '/'
        if contain_words == '':
            contain_words = False
        return contain_words

    df['key_drop'] = df['제목'].apply(is_contain_exception_word)
    return df


def sort_data_by_priority(df: pd.DataFrame) -> pd.DataFrame:
    effective_columns = ['제목', 'URL', '언론사', 'KeyWord', '포털명',
                         'key_drop', '언론사_is_black', '언론사_not_major']
    df = df[effective_columns]
    df = df.sort_values(by=['key_drop', '언론사_is_black', '언론사_not_major',
                            '제목'], kind='mergesort')
    df = df.reset_index(drop=True)
    return df


def check_identical_article(df: pd.DataFrame) -> pd.DataFrame:
    df['is_title_same'] = df.duplicated(subset=['제목'])
    return df


def sort_data_by_identical(df: pd.DataFrame) -> pd.DataFrame:
    effective_columns = ['제목', 'URL', '언론사', 'KeyWord', '포털명',
                         'key_drop', 'is_title_same', '언론사_is_black', '언론사_not_major']
    df = df[effective_columns]
    df = df.sort_values(by=['key_drop', 'is_title_same', '언론사_is_black', '언론사_not_major',
                            '제목'], kind='mergesort')
    df = df.reset_index(drop=True)
    return df


def check_similar_title(df: pd.DataFrame) -> pd.DataFrame:
    def get_effective_max_index(df):
        has_drop_keyword = (df['key_drop'] == False)
        is_title_same = (df['is_title_same'] == False)
        is_blacklist_media = (df['언론사_is_black'] == False)
        max_index = max(df[has_drop_keyword & is_title_same & is_blacklist_media].index)
        return max_index

    max_index_num = get_effective_max_index(df)
    max_index_num_for_indexing = max_index_num + 1
    titles = df['제목'].tolist()
    titles = titles[:max_index_num_for_indexing]

    model = SentenceTransformer('paraphrase-distilroberta-base-v1')
    embeddings = model.encode(titles, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)

    similarity_scores = cosine_scores.tolist()

    df['similarity'] = ''
    for title_number, row_data in enumerate(similarity_scores):
        result_similarity_score = 0
        result_comparison_number = 0
        for comparison_number, similarity_score in enumerate(row_data):
            # 전체를 비교할 필요 없이 절반만 비교한다.
            if title_number > comparison_number:
                # 유사도는 0.95/특정값 이상만 유의미할 때 적용
                if similarity_score > 0.95:
                    # 하나씩 비교하되 기존결과보다 클 경우에만 삽입
                    if similarity_score > result_similarity_score:
                        result_similarity_score = round(similarity_score, 2)
                        result_comparison_number = comparison_number
            else:
                continue
        compared_title = df.at[result_comparison_number, '제목']
        if result_similarity_score != 0:
            result_text = f'유사도:{result_similarity_score},비교값:{result_comparison_number}-{compared_title}'
            df.at[title_number, 'similarity'] = result_text

    df['similarity'] = df['similarity'].apply(lambda x: False if x == '' else x)

    return df


def sort_data_by_similarity(df: pd.DataFrame) -> pd.DataFrame:
    effective_columns = ['제목', 'URL', '언론사', 'KeyWord', '포털명',
                         'key_drop', 'is_title_same', '언론사_is_black', 'similarity', '언론사_not_major']
    df = df[effective_columns]
    df = df.sort_values(by=['key_drop', 'is_title_same', '언론사_is_black', 'similarity', '언론사_not_major',
                            '제목'], kind='mergesort')
    df = df.reset_index(drop=True)
    return df


if __name__ == "__main__":
    # 앞단에서 도출된 데이터 사용
    result_file = r"d:\result.csv"
    df = pd.read_csv(result_file, encoding='UTF-8-SIG')


    # 실제 함수
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


    # 함수 실행
    df = correct_data(df)
    result_file = r"d:\result.csv"
    df.to_csv(result_file, encoding='UTF-8-SIG')
