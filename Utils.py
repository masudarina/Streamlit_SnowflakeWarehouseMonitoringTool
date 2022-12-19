##################################################
# モジュールインポート 
##################################################
import datetime
import snowflake.connector
import streamlit as st

##################################################
# デコレーター
##################################################

##################################################
# デコレーター名：print_log
#
# 機能概要：
# 関数処理にかかる時間をプリントするキャッシュ
##################################################
def print_log(func):

    def wrapper(*args, **kwargs):
        # 時間取得（デバッグ用）
        print('---- [START] ' + str(func.__name__) + ' date:' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        func(*args, **kwargs)
        # 時間取得（デバッグ用）
        print('---- [END] ' + str(func.__name__) + ' date:' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    return wrapper

##################################################
# デコレーター名：error_handling
#
# 機能概要：
# 関数処理にかかる時間をプリントするキャッシュ
##################################################
def error_handling(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except snowflake.connector.errors.ProgrammingError:
            st.error('''現在使用しているロールでは情報を表示できません''')
    return wrapper