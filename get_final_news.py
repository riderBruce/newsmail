import pandas as pd


def get_final_news(df: pd.DataFrame) -> pd.DataFrame:
    def get_effective_max_index(df):
        has_drop_keyword = (df['key_drop'] == False)
        is_title_same = (df['is_title_same'] == False)
        is_blacklist_media = (df['언론사_is_black'] == False)
        has_similar_title = (df['similarity'] == False)
        has_drop_keyword_inside_page = (df['text_drop'] == False)
        max_index = max(df[has_drop_keyword
                           & is_title_same
                           & is_blacklist_media
                           & has_similar_title
                           & has_drop_keyword_inside_page]
                        .index)
        return max_index

    max_index_num = get_effective_max_index(df)
    max_index_num_for_indexing = max_index_num + 1
    df.iloc[:max_index_num_for_indexing, 'mailing'] = True

    return df


def save_data(df: pd.DataFrame, result_file_name: str) -> None:
    try:
        save_news_excel(df, result_file_name)
    except Exception as ex:
        print(ex)

    # db에 해당 뉴스 저장


def get_mailing_data(df: pd.DataFrame) -> pd.DataFrame:
    df_for_mailing = df[df['mailing'] == True]

    return df_for_mailing


def save_news_excel(df: pd.DataFrame, result_file_name: str) -> None:
    df.to_excel(result_file_name)
    print(">> 엑셀 저장 완료")

