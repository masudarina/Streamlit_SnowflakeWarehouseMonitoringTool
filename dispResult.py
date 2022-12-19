##################################################
# モジュールインポート 
##################################################
import snowflake.connector
import pandas as pd
import streamlit as st
import altair as alt
from Utils import *

##################################################
# 関数
##################################################

###################################################
# 関数名：dispResult
#
# 機能概要：
# 引数を受け取ってSnowflakeでSQLを実行した結果で表を作成する
#
# 引数：
#   引数1:Snowfalke SQL実行のカーソル(cs:snowflake.connector.cursor.SnowflakeCursor型)
#   引数2:実行SQL(sql:str型)
#   引数3:データフレームのカラム(col:list型) 
#   引数4:データフレームのタイトル(subhead1:str型) 
#   引数5:データがない場合の表示文(info:str型) 
#   引数6:データフレームの表示方法(disptype:str型) 
#
# 戻り値：
#   戻り値1:データがない場合の表示文(st.info(info):streamlit.delta_generator.DeltaGenerator型)
#   戻り値2:第5引数がdataframeの場合のデータフレーム表示(st.dataframe(df1):streamlit.delta_generator.DeltaGenerator型)
# 　戻り値3:第5引数がtableの場合のデータフレーム表示st.dataframe(df1):streamlit.delta_generator.DeltaGenerator型)   
##################################################

@error_handling
def dispResult(cs,sql, col, info, disptype, subhead1):
    # SQL実行
    st.subheader(subhead1)
    result = cs.execute(sql).fetchall()
    columns1 = col
    if not result:
        # st.subheader(subhead1)
        return st.info(info)

    else:
        df1 = pd.DataFrame(data=result, columns=columns1) 
        df1.index = df1.index + 1
        # st.subheader(subhead1)
        if disptype == "table":
            return st.table(df1)
        if disptype == "dataframe":
            return st.dataframe(df1)

###################################################
# 関数名：showWarehouse
#
# 機能概要：
# Snowflakeでウェハウス一覧を表示するSQLを実行する
#
# 引数：
#   Snowfalke SQL実行のカーソル(cs:snowflake.connector.cursor.SnowflakeCursor型)
##################################################
@print_log
def showWarehouse(cs): 

    # SQL実行
    cs.execute("SHOW WAREHOUSES")

###################################################
# 関数名：exeFunc11~12
#
# 機能概要：
# 関数dispResultに引数を渡してSnowflakeでSQLを実行する
# (メニューの名前：セットアップ・構成の確認) 
#
# 引数：
#   Snowfalke SQL実行のカーソル(cs:snowflake.connector.cursor.SnowflakeCursor型)
#
# 戻り値：
#   なし 
##################################################

# ウェアハウス一覧
@print_log
def exeFunc11(cs):
    sql = '''SELECT "name", "size", "min_cluster_count", "max_cluster_count","scaling_policy", "auto_suspend", "auto_resume", "created_on", "resumed_on","owner", "comment" 
            FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) ORDER BY "size"'''
    col = ['WAREHOUSE_NAME', 'WAREHOUSE_SIZE', 'MIN_CLUSTER_COUNT', 'MAX_CLUSTER_COUNT', 'SCALING_POLICY', 'AUTO_SUSPENDED', 'AUTO_RESUME', 'CREATED_ON', 'RESUMED_ON', 'OWNER', 'COMMENT']
    subhead1 = "ウェアハウス一覧"
    info = "ウェアハウスが存在しません" 
    disptype = 'dataframe' 
    # st.write(str(sf_user))
    cs.execute("ALTER SESSION SET TIMEZONE = 'Asia/Tokyo'")
    showWarehouse(cs)
    dispResult(cs,sql, col, info, disptype, subhead1)

# 自動再開が有効になっているウェアハウス一覧
@print_log
def exeFunc12(cs):
    sql = '''SELECT "name", "size", "auto_resume" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) WHERE "auto_resume" = \'true\' ORDER BY "size"'''
    col = ['WAREHOUSE_NAME', 'WAREHOUSE_SIZE', 'AUTO_RESUME']
    subhead1 = "自動再開が有効になっているウェアハウス一覧"
    info = "自動再開が有効になっていないウェアハウスはありません"
    disptype = 'table'  
    showWarehouse(cs)
    dispResult(cs,sql, col, info, disptype, subhead1)

# 自動サスペンドが有効になっているウェアハウス一覧
@print_log
def exeFunc13(cs):
    sql = '''SELECT "name" AS WAREHOUSE_NAME ,"size" AS WAREHOUSE_SIZE FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) WHERE "auto_resume" = \'false\' ORDER BY "size"'''
    col = ['WAREHOUSE_NAME', 'WAREHOUSE_SIZE']
    subhead1 = "自動サスペンドが有効になっているウェアハウス一覧"
    info = "自動サスペンドが有効になっていないウェアハウスはありません" 
    disptype = 'table'  
    showWarehouse(cs)
    dispResult(cs,sql, col, info, disptype, subhead1)

# 自動停止時間が1分より長いウェアハウス一覧
@print_log
def exeFunc14(cs):
    sql = '''SELECT "name" ,"size","auto_suspend" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) WHERE "auto_suspend" > 60 ORDER BY "auto_suspend" DESC, "size" ASC '''
    col = ['WAREHOUSE_NAME', 'WAREHOUSE_SIZE', 'AUTOSUSPEND_TIME']
    subhead1 = "自動停止時間が1分より長いウェアハウス一覧"
    info = "自動停止時間が1分より長いウェアハウスはありません" 
    disptype = 'table'  
    showWarehouse(cs)
    dispResult(cs,sql, col, info, disptype, subhead1)

# 過去３０日間にログインしていないユーザー一覧
@print_log
def exeFunc15(cs):
    sql = '''SELECT NAME, LOGIN_NAME, OWNER, DEFAULT_ROLE, LAST_SUCCESS_LOGIN FROM SNOWFLAKE.ACCOUNT_USAGE.USERS WHERE LAST_SUCCESS_LOGIN < DATEADD(MONTH, -1, CURRENT_TIMESTAMP()) 
            AND DELETED_ON IS NULL ORDER BY LAST_SUCCESS_LOGIN ASC'''
    col = ['USER_NAME', 'LOGIN_NAME', 'OWNER', 'DEFAULT_ROLE', 'LAST_LOGIN_DAY' ]
    subhead1 = "過去３０日間にログインしていないユーザー一覧"
    info = "過去３０日間にログインしていないユーザーはいません" 
    disptype = 'table'
    dispResult(cs,sql, col, info, disptype, subhead1)

# 未ログインユーザー一覧
@print_log
def exeFunc16(cs):
    sql = "SELECT NAME, LOGIN_NAME, OWNER, DEFAULT_ROLE, DEFAULT_WAREHOUSE, HAS_PASSWORD, CREATED_ON FROM SNOWFLAKE.ACCOUNT_USAGE.USERS WHERE LAST_SUCCESS_LOGIN IS NULL ORDER BY CREATED_ON"
    col = ['USER_NAME', 'LOGIN_NAME', 'OWNER', 'DEFAULT_ROLE', 'DEFAULT_WAREHOUSE', 'HAS_PASSWORD', 'CREATED_ON']
    subhead1 = "未ログインユーザー一覧"
    info = "未ログインユーザーはいません"
    disptype = 'dataframe'
    dispResult(cs,sql, col, info, disptype, subhead1)

# ステートメントタイムアウトの設定
@print_log
# def exeFunc17(cs, sf_user, sf_warehouse):
def exeFunc17(cs, sf_user, sf_warehouse):
    # アカウント
    st.subheader("ステートメントタイムアウトの設定")
    sql = "SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' IN ACCOUNT"
    col = ['KEY', 'VALUE', 'DEFAULT', 'LEVEL', 'DESCRIPTION', 'TYPE']
    subhead1 = "###### アカウント"
    info = "ステートメントタイムアウトの設定はありません"
    disptype = 'table'
    st.markdown(subhead1)
    result = cs.execute(sql).fetchall()
    columns1 = col
    if not result:
        # st.subheader(subhead1)
        st.info(info)
    else:
        df1 = pd.DataFrame(data=result, columns=columns1) 
        df1.index = df1.index + 1
        # st.subheader(subhead1)
        if disptype == "table":
            st.table(df1)
        if disptype == "dataframe":
            st.dataframe(df1)

    # ユーザー
    sql = "SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' IN USER" + " " + sf_user
    col = ['KEY', 'VALUE', 'DEFAULT', 'LEVEL', 'DESCRIPTION', 'TYPE']
    subhead1 = "###### ユーザー：" + sf_user 
    info = "ステートメントタイムアウトの設定はありません"
    disptype = 'table'
    st.markdown(subhead1)
    result = cs.execute(sql).fetchall()
    columns1 = col
    if not result:
        # st.subheader(subhead1)
        st.info(info)
    else:
        df1 = pd.DataFrame(data=result, columns=columns1) 
        df1.index = df1.index + 1
        if disptype == "table":
            st.table(df1)
        if disptype == "dataframe":
            st.dataframe(df1)

    # ウェアハウス
    if sf_warehouse:
        sql = "SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' IN WAREHOUSE" + " " + sf_warehouse
        col = ['KEY', 'VALUE', 'DEFAULT', 'LEVEL', 'DESCRIPTION', 'TYPE']
        subhead1 = "###### ウェアハウス：" + sf_warehouse
        info = "ステートメントタイムアウトの設定はありません"
        disptype = 'table'

        st.markdown(subhead1)
        result = cs.execute(sql).fetchall()
        columns1 = col
        if not result:
            st.info(info)

        else:
            df1 = pd.DataFrame(data=result, columns=columns1) 
            df1.index = df1.index + 1
            if disptype == "table":
                st.table(df1)
            if disptype == "dataframe":
                st.dataframe(df1)

    else:
        sf_current_warehouse = cs.execute("SELECT CURRENT_WAREHOUSE()").fetchall()
        st1 = str(sf_current_warehouse)[3:]
        st2 = st1[:-4]
        if st2 == "on":
            st3 = " "
            sql = "SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' IN WAREHOUSE" + " " + st3
            col = ['KEY', 'VALUE', 'DEFAULT', 'LEVEL', 'DESCRIPTION', 'TYPE']
            subhead1 = "###### ウェアハウス：" + st3 
            info = "ステートメントタイムアウトの設定はありません"
            disptype = 'table'

            st.markdown(subhead1)
            result = cs.execute(sql).fetchall()
            columns1 = col
            if not result:
                st.info(info)
            else:
                df1 = pd.DataFrame(data=result, columns=columns1) 
                df1.index = df1.index + 1
                if disptype == "table":
                    st.table(df1)
                if disptype == "dataframe":
                    st.dataframe(df1)
        else:
            sql = "SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' IN WAREHOUSE" + " " + st2
            col = ['KEY', 'VALUE', 'DEFAULT', 'LEVEL', 'DESCRIPTION', 'TYPE']
            subhead1 = "###### ウェアハウス：" + st2 
            info = "ステートメントタイムアウトの設定はありません"
            disptype = 'table'

            st.markdown(subhead1)
            result = cs.execute(sql).fetchall()
            columns1 = col
            if not result:
                st.info(info)
            else:
                df1 = pd.DataFrame(data=result, columns=columns1) 
                df1.index = df1.index + 1
                if disptype == "table":
                    st.table(df1)
                if disptype == "dataframe":
                    st.dataframe(df1)

# 過去７日間で失敗したタスク一覧
@print_log
def exeFunc18(cs):
    sql = '''SELECT NAME, DATABASE_NAME, STATE, QUERY_TEXT, QUERY_START_TIME, ERROR_CODE, ERROR_MESSAGE 
            FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY WHERE STATE = 'FAILED' AND QUERY_START_TIME >= DATEADD (DAY, -7, CURRENT_TIMESTAMP()) ORDER BY QUERY_START_TIME DESC'''
    col = ['WAREHOUSE_NAME', 'LOGIN_NAME', 'OWNER', 'DEFAULT_ROLE', 'HAS_PASSWORD', 'CREATED_ON']
    subhead1 ="過去７日間で失敗したタスク一覧"
    info = "過去７日間で失敗したタスクはありません"
    disptype = 'table'
    dispResult(cs,sql, col, info, disptype, subhead1)

# 過去７日間で長時間実行されたタスク一覧
@print_log
def exeFunc19(cs):
    sql = '''SELECT DATEDIFF(SECONDS, QUERY_START_TIME,COMPLETED_TIME) AS DURATION_SECONDS , NAME, DATABASE_NAME, QUERY_TEXT, STATE, QUERY_START_TIME 
           FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY WHERE STATE = 'SUCCEEDED' AND QUERY_START_TIME >= DATEADD (DAY, -7, CURRENT_TIMESTAMP()) ORDER BY DURATION_SECONDS DESC'''
    col =  ['DURATION_SECONDS', 'NAME', 'DATABASE_NAME', 'QUERY_TEXT', 'STATE', 'QUERY_START_TIME']
    subhead1 ="過去７日間で長時間実行されたタスク一覧"
    info = "過去７日間で長時間実行されたタスクはありません"
    disptype = 'table'
    dispResult(cs,sql, col, info, disptype, subhead1)

###################################################
# 関数名：exeFunc21~24
#
# 機能概要：
# 関数dispResultに引数を渡してSnowflakeでSQLを実行する
# (メニューの名前：利用状況確認)
#
# 引数：
#   Snowfalke SQL実行のカーソル(cs:snowflake.connector.cursor.SnowflakeCursor型)
#
# 戻り値：
#   なし
##################################################

# ウェアハウス別のクレジット使用（過去７日間）
@print_log
def exeFunc21(cs):
# 過去７日の表
    col = ['WAREHOUSE_NAME', 'CREDITS_USED_COMPUTE_SUM']
    sql = '''SELECT WAREHOUSE_NAME ,CAST(SUM(CREDITS_USED_COMPUTE) AS FLOAT) AS CREDITS_USED_COMPUTE_SUM 
            FROM ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY WHERE START_TIME >= TO_DATE(DATEADD(DAY, -7, CURRENT_TIMESTAMP()))  GROUP BY 1 ORDER BY 2 DESC'''
    subhead1 = 'ウェアハウス別のクレジット使用（過去７日間）'
    info = '過去７日間でクレジットが使用されたウェアハウスがありません'
    disptype = 'table'
    try:
        cs.execute("USE SCHEMA SNOWFLAKE.ACCOUNT_USAGE").fetchall()
        dispResult(cs, sql, col, info, disptype, subhead1)

        #  ウェアハウス別のグラフ
        data1 = cs.execute(sql).fetchall()
        df = pd.DataFrame(data = data1, columns = col)
        chart = alt.Chart(df).mark_bar().encode(
        alt.X('WAREHOUSE_NAME', sort=None, title = 'ウェアハウス'),
        alt.Y('CREDITS_USED_COMPUTE_SUM',title = 'クレジット'),
        tooltip=[ alt.Tooltip("WAREHOUSE_NAME", title="ウェアハウス"), alt.Tooltip("CREDITS_USED_COMPUTE_SUM", title="クレジット"), ]
        )
        st.caption("ウェアハウス別のグラフ")
        st.altair_chart(chart, use_container_width=True)

        # 過去７日のグラフ　積み上げ棒グラフ
        data1 = cs.execute('''SELECT * FROM ( 
            SELECT  
                CURRENT_DATE() AS LABEL,  
                WAREHOUSE_NAME AS WAREHOUSE_NAME,  
                CAST(SUM(CREDITS_USED_COMPUTE) AS FLOAT) AS CREDITS_USED_COMPUTE_SUM 
            FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" 
            WHERE TO_DATE(START_TIME) >= TO_DATE(CURRENT_DATE())  
            GROUP BY 1,2
            ORDER BY 1 DESC 
            ) 
            UNION ALL
            SELECT * FROM (
                SELECT
                DATEADD('DAY', -1, CURRENT_DATE()) AS LABEL,  
                WAREHOUSE_NAME AS WAREHOUSE_NAME,  
                SUM(CREDITS_USED_COMPUTE) AS CREDITS_USED_COMPUTE_SUM 
                FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" 
                WHERE TO_DATE(START_TIME) = TO_DATE(DATEADD(DAY, -1, CURRENT_DATE()))  
                GROUP BY 1,2
                ORDER BY 1 DESC 
            ) 
            UNION ALL 
            SELECT * FROM ( 
                SELECT  
                    DATEADD('DAY', -2, CURRENT_DATE()) AS LABEL,  
                    WAREHOUSE_NAME AS WAREHOUSE_NAME,  
                    SUM(CREDITS_USED_COMPUTE) AS CREDITS_USED_COMPUTE_SUM 
                FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" 
                WHERE TO_DATE(START_TIME) = TO_DATE(DATEADD(DAY, -2, CURRENT_DATE())) 
                GROUP BY 1,2
            ORDER BY 1 DESC 
            ) 
            UNION ALL 
            SELECT * FROM ( 
                SELECT  
                    DATEADD('DAY', -3, CURRENT_DATE()) AS LABEL,  
                    WAREHOUSE_NAME AS WAREHOUSE_NAME,  
                    CAST(SUM(CREDITS_USED_COMPUTE) AS FLOAT) AS CREDITS_USED_COMPUTE_SUM 
                FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" 
                WHERE TO_DATE(START_TIME) = TO_DATE(DATEADD(DAY, -3, CURRENT_DATE()))  
                GROUP BY 1,2
            ORDER BY 1 DESC 
            ) 
            UNION ALL 
            SELECT * FROM ( 
                SELECT  
                    DATEADD('DAY', -4, CURRENT_DATE()) AS LABEL,  
                    WAREHOUSE_NAME AS WAREHOUSE_NAME,  
                    CAST(SUM(CREDITS_USED_COMPUTE) AS FLOAT) AS CREDITS_USED_COMPUTE_SUM 
                FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" 
                WHERE TO_DATE(START_TIME) = TO_DATE(DATEADD(DAY, -4, CURRENT_DATE()))  
                GROUP BY 1,2
            ORDER BY 1 DESC 
            ) 
            UNION ALL 
            SELECT * FROM ( 
                SELECT  
                    DATEADD('DAY', -5, CURRENT_DATE()) AS LABEL,  
                    WAREHOUSE_NAME AS WAREHOUSE_NAME,  
                    CAST(SUM(CREDITS_USED_COMPUTE) AS FLOAT) AS CREDITS_USED_COMPUTE_SUM 
                FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" 
                WHERE TO_DATE(START_TIME) = TO_DATE(DATEADD(DAY, -5, CURRENT_DATE())) 
                GROUP BY 1,2
            ORDER BY 1 DESC 
            ) 
            UNION ALL 
            SELECT * FROM ( 
                SELECT  
                    DATEADD('DAY', -6, CURRENT_DATE()) AS LABEL, 
                    WAREHOUSE_NAME AS WAREHOUSE_NAME,  
                    CAST(SUM(CREDITS_USED_COMPUTE) AS FLOAT) AS CREDITS_USED_COMPUTE_SUM 
                FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" 
                WHERE TO_DATE(START_TIME) = TO_DATE(DATEADD(DAY, -6, CURRENT_DATE()))  
                GROUP BY 1,2
            ORDER BY 1 DESC 
            ) 
            UNION ALL 
            SELECT * FROM ( 
                SELECT  
                    DATEADD('DAY', -7, CURRENT_DATE()) AS LABEL, 
                    WAREHOUSE_NAME AS WAREHOUSE_NAME,  
                    CAST(SUM(CREDITS_USED_COMPUTE) AS FLOAT) AS CREDITS_USED_COMPUTE_SUM 
                FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" 
                WHERE TO_DATE(START_TIME) = TO_DATE(DATEADD(DAY, -7, CURRENT_DATE()))  
                GROUP BY 1,2
                ORDER BY 1 DESC 
        )''').fetchall()
        df = pd.DataFrame(data1, columns = ["day", "warehouse", "data"])
        chart = alt.Chart(df).mark_bar().encode(
        alt.X("yearmonthdate(day):N", title = '日付', axis=alt.Axis(format="%Y-%m-%d")),
        alt.Y("data", title = 'クレジット'),
        alt.Color("warehouse",title = 'ウェアハウス'),
        tooltip=[ alt.Tooltip("yearmonthdate(day):N", title="日付"), alt.Tooltip("data", title="クレジット"), alt.Tooltip("warehouse", title="ウェアハウス"), ]
        )
        st.caption("日別のグラフ")
        st.altair_chart(chart, use_container_width=True)

    except snowflake.connector.errors.ProgrammingError:
        st.subheader(subhead1)
        st.error('''現在使用しているロールでは情報を表示できません''')

    # ウェアハウス別のクレジット使用（過去４週間）

    # 過去４週間の表
    col = ['WAREHOUSE_NAME', 'CREDITS_USED_COMPUTE_SUM']
    sql = '''SELECT WAREHOUSE_NAME ,CAST(SUM(CREDITS_USED_COMPUTE) AS FLOAT) AS CREDITS_USED_COMPUTE_SUM 
            FROM ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY WHERE START_TIME >= DATEADD(WEEK, -4, CURRENT_TIMESTAMP())  GROUP BY 1 ORDER BY 2 DESC'''
    subhead1 = 'ウェアハウス別のクレジット使用（過去４週間）'
    info = '過去７日間でクレジットが使用されたウェアハウスがありません'
    disptype = 'table'
    try:
        cs.execute("USE SCHEMA SNOWFLAKE.ACCOUNT_USAGE").fetchall()
        dispResult(cs, sql, col, info, disptype, subhead1)

        # 過去４週間のグラフ
        data1 = cs.execute(sql)
        df = pd.DataFrame(data = data1, columns = col)
        # pv=df.pivot_table(index = "WAREHOUSE_NAME")
        chart = alt.Chart(df).mark_bar().encode(
        alt.X('WAREHOUSE_NAME', sort=None, title = "ウェアハウス"),
        alt.Y('CREDITS_USED_COMPUTE_SUM', title = "クレジット"),
        tooltip=[ alt.Tooltip("CREDITS_USED_COMPUTE_SUM", title="クレジット"), alt.Tooltip("WAREHOUSE_NAME", title="ウェアハウス"), ]
        )
        st.caption("ウェアハウス別のグラフ")
        st.altair_chart(chart, use_container_width=True)

        # 過去４週間のグラフ　積み上げ棒グラフ
        data1 = cs.execute(
            '''SELECT * FROM (
            SELECT  
                DATEADD('DAY', -7, CURRENT_DATE()) || '~' || CURRENT_DATE() AS LABEL,  
                WAREHOUSE_NAME AS WAREHOUSE_NAME, 
                CAST(SUM(CREDITS_USED_COMPUTE) AS FLOAT) AS CREDITS_USED_COMPUTE_SUM 
                FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" 
                WHERE START_TIME >= DATEADD(WEEK, -1, CURRENT_TIMESTAMP())  
                GROUP BY 2 ORDER BY 3 DESC ) 
            UNION ALL 
            SELECT * FROM ( 
                    SELECT  
                    DATEADD('DAY', -14, CURRENT_DATE()) || '~' || DATEADD('DAY', -8, CURRENT_DATE()) AS LABEL, 
                    WAREHOUSE_NAME AS WAREHOUSE_NAME, 
                    CAST(SUM(CREDITS_USED_COMPUTE) AS FLOAT) AS CREDITS_USED_COMPUTE_SUM 
                FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" 
                WHERE START_TIME BETWEEN DATEADD(WEEK, -2, CURRENT_TIMESTAMP())  AND DATEADD(WEEK, -1, CURRENT_TIMESTAMP()) 
                GROUP BY 2  ORDER BY 3 DESC ) 
            UNION ALL 
            SELECT * FROM ( 
                    SELECT  DATEADD('DAY', -21, CURRENT_DATE()) || '~' || DATEADD('DAY', -15, CURRENT_DATE()) AS LABEL, 
                    WAREHOUSE_NAME AS WAREHOUSE_NAME, 
                    CAST(SUM(CREDITS_USED_COMPUTE) AS FLOAT) AS CREDITS_USED_COMPUTE_SUM 
                FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" 
                WHERE START_TIME BETWEEN DATEADD(WEEK, -3, CURRENT_TIMESTAMP())  AND DATEADD(WEEK, -2, CURRENT_TIMESTAMP()) 
                GROUP BY 2  ORDER BY 3 DESC ) 
            UNION ALL 
            SELECT * FROM ( 
                    SELECT  DATEADD('DAY', -28, CURRENT_DATE()) || '~' || DATEADD('DAY', -22, CURRENT_DATE()) AS LABEL, 
                    WAREHOUSE_NAME AS WAREHOUSE_NAME, 
                    CAST(SUM(CREDITS_USED_COMPUTE) AS FLOAT) AS CREDITS_USED_COMPUTE_SUM 
                FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" 
                WHERE START_TIME BETWEEN DATEADD(WEEK, -4, CURRENT_TIMESTAMP())  AND DATEADD(WEEK, -3, CURRENT_TIMESTAMP()) 
                GROUP BY 2  ORDER BY 3 DESC ) ORDER BY 1''').fetchall()
        df = pd.DataFrame(data1, columns = ["week", "warehouse", "data"])
        chart = alt.Chart(df).mark_bar().encode(
        alt.X('week', title = "期間"),
        alt.Y('data', title = "クレジット"),
        alt.Color('warehouse', title = "ウェアハウス"),
        tooltip=[ alt.Tooltip("week", title="期間"), alt.Tooltip("data", title="クレジット"), alt.Tooltip("warehouse", title="ウェアハウス"), ]
        )
        st.caption("週別のグラフ")
        st.altair_chart(chart, use_container_width=True)

    except snowflake.connector.errors.ProgrammingError:
        st.subheader(subhead1)
        st.error('''現在使用しているロールでは情報を表示できません''')

# １時間ごとのウェアハウス別のクレジット使用（過去3日間）
@print_log
def exeFunc22(cs):
    try:
        # 表作成
        col = ['START_TIME', 'WAREHOUSE_NAME', 'CREDITS_USED_COMPUTE']
        sql = '''SELECT START_TIME ,WAREHOUSE_NAME , CAST(CREDITS_USED_COMPUTE AS FLOAT) AS CREDITS_USED_COMPUTE 
                FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY WHERE START_TIME >= DATEADD(DAY, -3, CURRENT_TIMESTAMP())  AND WAREHOUSE_ID > 0   ORDER BY 1 DESC,2'''
        subhead1 = '１時間ごとのウェアハウス別のクレジット使用（過去３日間）'
        info = '過去３日間でクレジットが使用されたウェアハウスがありません'
        disptype = 'dataframe'
        cs.execute("USE SCHEMA SNOWFLAKE.ACCOUNT_USAGE").fetchall()
        dispResult(cs, sql, col, info, disptype, subhead1) 

        # グラフ作成
        data1 = cs.execute(sql).fetchall()
        df = pd.DataFrame(data1, columns = ["hours", "warehouse", "data"])
        chart = alt.Chart(df).mark_bar().encode(
        # alt.X('yearmonthdatehours(hours):N', title = "時間", axis=alt.Axis(format="%Y-%m-%d %H:%M"), timeUnit= "yearmonthdatehours"),
        alt.X('yearmonthdatehours(hours):T', title = "時間", axis=alt.Axis(format="%Y-%m-%d %H:%M")),
        alt.Y('data', title = "クレジット"),
        alt.Color('warehouse', title = "ウェアハウス"),
        tooltip=[ alt.Tooltip("hours", title="期間"), alt.Tooltip("data", title="クレジット"), alt.Tooltip("warehouse", title="ウェアハウス"), ]
        )
        # st.error(" X 軸が１時間ごとに表示されない")
        st.altair_chart(chart, use_container_width=True)

    except snowflake.connector.errors.ProgrammingError:
        st.subheader(subhead1)
        st.error('''現在使用しているロールでは情報を表示できません''')

# １時間ごとのクエリ数（過去７日間）
@print_log
def exeFunc23(cs):
    col = ['QUERY_START_HOUR', 'WAREHOUSE_NAME', 'NUM_QUERIES']
    sql = '''SELECT DATE_TRUNC('HOUR', START_TIME) AS QUERY_START_HOUR ,WAREHOUSE_NAME ,COUNT(*) AS NUM_QUERIES  
            FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY WHERE START_TIME >= DATEADD(DAY, -7, CURRENT_TIMESTAMP())  GROUP BY 1, 2 ORDER BY 1 DESC, 2'''
    subhead1 = '１時間ごとのクエリ数（過去７日間）'
    info = '過去７日間でクエリが実行されていません'
    disptype = 'dataframe'
    dispResult(cs, sql, col, info, disptype, subhead1)

# 過去１年間の数週間にわたるウェアハウスのクレジット消費の異常を特定
@print_log
def exeFunc24(cs):
    col = ['START_DATE', 'WAREHOUSE_NAME', 'CREDITS_USED_DATE_WH', 'CREDITS_USED_7_DAY_AVG', 'PCT_OVER_TO_7_DAY_AVERAGE']
    sql = '''WITH CTE_DATE_WH AS( 
        SELECT 
            TO_DATE(START_TIME) AS START_DATE , 
            WAREHOUSE_NAME ,CAST(SUM(CREDITS_USED) AS FLOAT) AS CREDITS_USED_DATE_WH 
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY GROUP BY START_DATE ,WAREHOUSE_NAME ) 
        SELECT 
            START_DATE , 
            WAREHOUSE_NAME  , 
            CAST(CREDITS_USED_DATE_WH AS FLOAT) , 
            CAST(AVG(CREDITS_USED_DATE_WH) OVER (PARTITION BY WAREHOUSE_NAME ORDER BY START_DATE ROsc 7 PRECEDING) AS FLOAT) AS CREDITS_USED_7_DAY_AVG ,
            CAST(100.0*((CREDITS_USED_DATE_WH / CREDITS_USED_7_DAY_AVG) - 1) AS FLOAT) AS PCT_OVER_TO_7_DAY_AVERAGE 
        FROM CTE_DATE_WH QUALIFY CREDITS_USED_DATE_WH > 100    AND PCT_OVER_TO_7_DAY_AVERAGE >= 0.5 
        ORDER BY PCT_OVER_TO_7_DAY_AVERAGE DESC'''
    subhead1 = '過去１年間の数週間にわたるウェアハウスのクレジット消費の異常を特定'
    info = '過去1年間の数週間にわたるウェアハウスのクレジット消費の異常はありません'
    disptype = 'dataframe'
    dispResult(cs, sql, col, info, disptype, subhead1)
    st.write("※１週間でクレジット消費が５０%以上増加した場合を異常と判断する")

###################################################
# 関数名：exeFunc31~36
#

# 機能概要：
# 関数dispResultに引数を渡してSnowflakeでSQLを実行する
# (メニューの名前：パフォーマンス状況確認)
#
# 引数：
#   Snowfalke SQL実行のカーソル(cs:snowflake.connector.cursor.SnowflakeCursor型)
#
# 戻り値：
#   なし 
##################################################

# 大量のデータをスキャンするクエリを実行しているユーザー一覧 （過去４５日間）
@print_log
def exeFunc31(cs):
    col = ['USER_NAME', 'WAREHOUSE_NAME', 'AVG_PCT_SCANNED']
    sql = '''SELECT USER_NAME, WAREHOUSE_NAME, CAST(AVG(CASE WHEN PARTITIONS_TOTAL > 0 THEN PARTITIONS_SCANNED / PARTITIONS_TOTAL ELSE 0 END) AS FLOAT) AVG_PCT_SCANNED 
            FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY WHERE START_TIME::DATE > DATEADD('DAYS', -45, CURRENT_DATE)GROUP BY 1, 2 ORDER BY 3 DESC'''
    subhead1 = '大量のデータをスキャンするクエリを実行しているユーザー一覧 （過去４５日間）'
    info = '過去４５日間で大量のデータをスキャンするクエリを実行しているユーザはいません'
    disptype = 'table'
    dispResult(cs, sql, col, info, disptype, subhead1)

# リモートストレージに流出したバイト数の観点から、問題のあるクエリ一覧（過去４５日間 / 上位１０件のクエリ）
@print_log
def exeFunc32(cs):
    col = ['QUERY_ID', 'PARTIAL_QUERY_TEXT', 'USER_NAME', 'WAREHOUSE_NAME', 'WAREHOUSE_SIZE', 'BYTES_SPILLED_TO_REMOTE_STORAGE', 'START_TIME', 'END_TIME', 'TOTAL_ELAPSED_TIME']
    sql = '''SELECT 
                QUERY_ID, 
                SUBSTR(QUERY_TEXT, 1, 50) PARTIAL_QUERY_TEXT, 
                USER_NAME, WAREHOUSE_NAME, 
                WAREHOUSE_SIZE,  
                BYTES_SPILLED_TO_REMOTE_STORAGE, 
                START_TIME, 
                END_TIME, 
                CAST(TOTAL_ELAPSED_TIME/1000 AS FLOAT) AS TOTAL_ELAPSED_TIME 
            FROM  SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY 
            WHERE  BYTES_SPILLED_TO_REMOTE_STORAGE > 0 AND START_TIME::DATE > DATEADD('DAYS', -45, CURRENT_DATE) 
            ORDER  BY BYTES_SPILLED_TO_REMOTE_STORAGE DESC LIMIT 10'''
    subhead1 = 'リモートストレージに流出したバイト数の観点から、問題のあるクエリ一覧（過去４５日間 / 上位１０件のクエリ）'
    info = '過去４５日間でリモートストレージに流出したバイト数の観点から、問題のあるクエリはありません'
    disptype = 'dataframe'
    dispResult(cs, sql, col, info, disptype, subhead1)

# 過去 1 年間に自動クラスタリングによって消費された 1 日の平均クレジットの一覧
@print_log
def exeFunc33(cs):
    col = ['DATE_TRUNC(WEEK,DATE)', 'AVG_DAILY_CREDITS']
    sql = '''WITH CREDITS_BY_DAY AS ( 
            SELECT 
                TO_DATE(START_TIME) AS DATE ,
                CAST(SUM(CREDITS_USED) AS FLOAT) AS CREDITS_USED 
            FROM "SNOWFLAKE"."ACCOUNT_USAGE"."AUTOMATIC_CLUSTERING_HISTORY" 
            WHERE START_TIME >= DATEADD(YEAR,-1,CURRENT_TIMESTAMP())  
            GROUP BY 1 ORDER BY 2 DESC  ) 
            SELECT 
                DATE_TRUNC('WEEK',DATE) ,
                CAST(AVG(CREDITS_USED) AS FLOAT) AS AVG_DAILY_CREDITS 
            FROM CREDITS_BY_DAY GROUP BY 1 ORDER BY 1'''
    subhead1 = '過去 1 年間に自動クラスタリングによって消費された 1 日の平均クレジットの一覧'
    info = '過去 1 年間に自動クラスタリングによって消費されたクレジットはありません'
    disptype = 'table'
    dispResult(cs, sql, col, info, disptype, subhead1)

# マテリアライズドビューが過去１年間に消費した１日の平均クレジットの一覧
@print_log
def exeFunc34(cs):
    col = ['DATE_TRUNC(WEEK,DATE)', 'AVG_DAILY_CREDITS']
    sql = '''WITH CREDITS_BY_DAY AS ( 
            SELECT 
                TO_DATE(START_TIME) AS DATE ,
                CAST(SUM(CREDITS_USED) AS FLOAT) AS CREDITS_USED 
            FROM "SNOWFLAKE"."ACCOUNT_USAGE"."MATERIALIZED_VIEW_REFRESH_HISTORY" 
            WHERE START_TIME >= DATEADD(YEAR,-1,CURRENT_TIMESTAMP())  
            GROUP BY 1 ORDER BY 2 DESC  ) 
            SELECT 
                DATE_TRUNC('WEEK',DATE) ,
                CAST(AVG(CREDITS_USED) AS FLOAT) AS AVG_DAILY_CREDITS 
            FROM CREDITS_BY_DAY GROUP BY 1 ORDER BY 1'''
    subhead1 = 'マテリアライズドビューが過去１年間に消費した１日の平均クレジットの一覧'
    info = 'マテリアライズドビューが過去１年間に消費したクレジットはありません'
    disptype = 'table'
    dispResult(cs, sql, col, info, disptype, subhead1)

# 過去１年間の検索最適化サービス(SOS)履歴と7日間平均の一覧
@print_log
def exeFunc35(cs):
    col = ['DATE_TRUNC(WEEK,DATE)', 'AVG_DAILY_CREDITS']
    sql = '''WITH CREDITS_BY_DAY AS ( 
        SELECT 
            TO_DATE(START_TIME) AS DATE ,
            CAST(SUM(CREDITS_USED) AS FLOAT) AS CREDITS_USED 
        FROM "SNOWFLAKE"."ACCOUNT_USAGE"."SEARCH_OPTIMIZATION_HISTORY"
        WHERE START_TIME >= DATEADD(YEAR,-1,CURRENT_TIMESTAMP())  GROUP BY 1 ORDER BY 2 DESC  ) 
        SELECT 
            DATE_TRUNC('WEEK',DATE) ,
            CAST(AVG(CREDITS_USED) AS FLOAT) AS AVG_DAILY_CREDITS 
        FROM CREDITS_BY_DAY GROUP BY 1 ORDER BY 1'''
    subhead1 = '過去１年間の検索最適化サービス(SOS)履歴と7日間平均の一覧'
    info = '過去１年間の検索最適化サービス(SOS)履歴はありません'
    disptype = 'table'
    dispResult(cs, sql, col, info, disptype, subhead1)

# Snowpipe が過去 1 年間に消費した 1 日の平均クレジットの一覧
@print_log
def exeFunc36(cs):
    col = ['DATE_TRUNC(WEEK,DATE)', 'AVG_DAILY_CREDITS']
    sql = '''WITH CREDITS_BY_DAY AS ( 
        SELECT 
            TO_DATE(START_TIME) AS DATE ,
            CAST(SUM(CREDITS_USED) AS FLOAT) AS CREDITS_USED 
        FROM "SNOWFLAKE"."ACCOUNT_USAGE"."PIPE_USAGE_HISTORY" 
        WHERE START_TIME >= DATEADD(YEAR,-1,CURRENT_TIMESTAMP())  GROUP BY 1 ORDER BY 2 DESC  ) 
        SELECT 
            DATE_TRUNC('WEEK',DATE) ,
            CAST(AVG(CREDITS_USED) AS FLOAT) AS AVG_DAILY_CREDITS 
        FROM CREDITS_BY_DAY GROUP BY 1 ORDER BY 1'''
    subhead1 = 'Snowpipe が過去 1 年間に消費した 1 日の平均クレジットの一覧'
    info = 'Snowpipe が過去 1 年間に消費したクレジットはありません'
    disptype = 'table'
    dispResult(cs, sql, col, info, disptype, subhead1)

###################################################
# 関数名：exeFunc 41~44
#
# 機能概要：
# 関数dispResultに引数を渡してSnowflakeでSQLを実行する
# (メニューの名前：コスト確認)
#
# 引数：
#   Snowfalke SQL実行のカーソル(cs:snowflake.connector.cursor.SnowflakeCursor型)
#
# 戻り値：
#   なし 
##################################################

# 日付ごとの利用グラフ
@print_log
def exeFunc41(cs):
    with st.form('my_form_exefunc41'):
        st.subheader("日付ごとのタイプ別利用一覧")
        st.write("▼期間とUSAGEの単価を変更できます")
        slider_date = st.slider('　期間を変更', 0, 100, 30)
        col1, col2 = st.columns(2)
        with col1:
            text_metering = st.number_input("METERING_DAILY_HISTORYのUSAGEの単価を変更" , value=5.7)
        with col2:
            text_storage = st.number_input("STORAGE_USAGEのUSAGEの単価を変更", value=25)
        text_storage = str(text_storage)
        text_metering = str(text_metering)
        st.form_submit_button("Submit") 

        sql = '''SELECT MDH.USAGE_DATE DATE ,CAST(SUM(MDH.CREDITS_BILLED)AS FLOAT) CREDIT, CREDIT * ''' + text_metering +  '''USAGE, 'METERING_DAILY_HISTORY' TYPE 
            FROM "SNOWFLAKE"."ACCOUNT_USAGE"."METERING_DAILY_HISTORY" MDH
            WHERE MDH.USAGE_DATE > CURRENT_DATE() -''' + str(slider_date) + '''GROUP BY MDH.USAGE_DATE,SERVICE_TYPE
            UNION ALL
            SELECT SH.USAGE_DATE DATE ,CAST(SUM(SH.STORAGE_BYTES + SH.STAGE_BYTES + SH.FAILSAFE_BYTES)/1000/1000/1000/1000 AS FLOAT) CREDIT, CREDIT*''' + text_storage + ''', 'STORAGE_USAGE' TYPE  
            FROM "SNOWFLAKE"."ACCOUNT_USAGE"."STORAGE_USAGE" SH
            WHERE SH.USAGE_DATE > CURRENT_DATE() -'''  + str(slider_date) +  '''GROUP BY SH.USAGE_DATE ORDER BY DATE DESC'''
        col = ['DATE', 'CREDIT', 'USAGE', 'TYPE']
        subhead1 ="過去" + str(slider_date) + "日間のタイプ別利用一覧"
        info = "過去" + str(slider_date) + "日間の間にクレジットは消費されていません"
        disptype = 'dataframe'
        cs.execute("ALTER SESSION SET TIMEZONE = 'Asia/Tokyo'")
        st.write(subhead1)

        result = cs.execute(sql).fetchall()
        columns1 = col
        if not result:
            st.info(info)

        else:
            df1 = pd.DataFrame(data=result, columns=columns1) 
            df1.index = df1.index + 1
            if disptype == "table":
                st.table(df1)
            if disptype == "dataframe":
                st.dataframe(df1)

        # グラフ作成
        try:
            data1 = cs.execute('''SELECT MDH.USAGE_DATE DATE ,CAST(SUM(MDH.CREDITS_BILLED)AS FLOAT) CREDIT, 'METERING_DAILY_HISTORY' TYPE 
                    FROM "SNOWFLAKE"."ACCOUNT_USAGE"."METERING_DAILY_HISTORY" MDH
                    WHERE MDH.USAGE_DATE > CURRENT_DATE()  -''' + str(slider_date) + ''' GROUP BY MDH.USAGE_DATE,SERVICE_TYPE
                    UNION ALL
                    SELECT SH.USAGE_DATE DATE ,CAST(SUM(SH.STORAGE_BYTES + SH.STAGE_BYTES + SH.FAILSAFE_BYTES)/1000/1000/1000/1000 AS FLOAT) CREDIT, 'STORAGE_USAGE' TYPE  
                    FROM "SNOWFLAKE"."ACCOUNT_USAGE"."STORAGE_USAGE" SH
                    WHERE SH.USAGE_DATE > CURRENT_DATE()  - ''' + str(slider_date) +  ''' GROUP BY SH.USAGE_DATE ORDER BY DATE DESC'''
                    ).fetchall()
        except snowflake.connector.errors.ProgrammingError:
            pass
        else:
            df = pd.DataFrame(data1, columns = ["day", "credit", "type"])
            chart = alt.Chart(df).mark_bar().encode(
            alt.X("yearmonthdate(day):N", title = '日付', axis=alt.Axis(format="%Y-%m-%d")),
            alt.Y("credit", title = 'クレジット'),
            alt.Color("type",title = 'タイプ'),
            tooltip=[ alt.Tooltip("yearmonthdate(day):N", title="日付"), alt.Tooltip("credit", title="クレジット"), alt.Tooltip("type", title="タイプ"), ]
            )
            st.write("日別のグラフ")
            st.altair_chart(chart, use_container_width=True)
            st.caption("( METERING_DAILY_HISTORYの単価 = " + text_metering + " , STORAGE_USAGEの単価 = " + text_storage + " )")

# 期間ごとのウェアハウス別クレジット一覧
@print_log
def exeFunc42(cs):
    with st.form('form_exefunc42'):
        st.subheader("期間ごとのウェアハウス別クレジット一覧")
        st.write("▼期間を変更できます")
        slider_date = st.slider('　期間を選択できます', 0, 100, 30)
        st.form_submit_button("Submit")
        col = ['DAY', 'CREDIT', 'WAREHOUSE_NAME']
        sql = '''SELECT date(wmh.START_TIME) DAY ,CAST(sum(wmh.CREDITS_USED) AS FLOAT) AS CREDIT, wmh.WAREHOUSE_NAME 
                FROM "SNOWFLAKE"."ACCOUNT_USAGE"."WAREHOUSE_METERING_HISTORY" wmh 
                WHERE wmh.START_TIME >= CURRENT_DATE() - '''  + str(slider_date) + ''' GROUP BY DAY,wmh.WAREHOUSE_NAME ORDER BY DAY DESC'''
        info = '過去' + str(slider_date) + '日間でクレジットを消費したウェアハウスはありません'
        subhead1 = ' 過去' + str(slider_date) + '日間のウェアハウス別クレジット利用一覧'
        disptype = 'dataframe'
        st.write(subhead1)

        result = cs.execute(sql).fetchall()
        columns1 = col
        if not result:
            st.info(info)

        else:
            df1 = pd.DataFrame(data=result, columns=columns1) 
            df1.index = df1.index + 1
            if disptype == "table":
                st.table(df1)
            if disptype == "dataframe":
                st.dataframe(df1)

        # グラフ作成
        try:
            data1 = cs.execute(sql).fetchall()
        except snowflake.connector.errors.ProgrammingError:
            pass
        else:
            df = pd.DataFrame(data1, columns = ["day", "data", "warehouse"])
            chart = alt.Chart(df).mark_bar().encode(
            alt.X("yearmonthdate(day):N", title = '日付', axis=alt.Axis(format="%Y-%m-%d")),
            alt.Y("data", title = 'クレジット'),
            alt.Color("warehouse",title = 'ウェアハウス'),
            tooltip=[ alt.Tooltip("yearmonthdate(day):N", title="日付"), alt.Tooltip("data", title="クレジット"), alt.Tooltip("warehouse", title="ウェアハウス"), ]
            )
            st.write("日別のグラフ")
            st.altair_chart(chart, use_container_width=True)

# 過去30日間での高額なクエリ一覧
@print_log
def exeFunc43(cs):
    col = [ 'EXECUTION_TIME_SECONDS', 'QUERY_TEXT', 'USER_NAME', 'ROLE_NAME', 'WAREHOUSE_SIZE', 'NODES', 'QUERY_ID', 'QU', 'RELATIVE_PERFORMANCE_COST', 'EXECUTION_TIME_MILLISECONDS', 'EXECUTION_TIME_MINUTES', 'EXECUTION_TIME_HOURS', ]
    sql = '''WITH WAREHOUSE_SIZE AS ( 
        SELECT 
            WAREHOUSE_SIZE, 
            NODES 
        FROM ( 
            SELECT 
            'XSMALL' AS WAREHOUSE_SIZE,
            1 AS NODES 
            UNION ALL SELECT 'SMALL' AS WAREHOUSE_SIZE, 2 AS NODES 
            UNION ALL SELECT 'MEDIUM' AS WAREHOUSE_SIZE, 4 AS NODES 
            UNION ALL SELECT 'LARGE' AS WAREHOUSE_SIZE, 8 AS NODES 
            UNION ALL SELECT 'XLARGE' AS WAREHOUSE_SIZE, 16 AS NODES 
            UNION ALL SELECT '2XLARGE' AS WAREHOUSE_SIZE, 32 AS NODES 
            UNION ALL SELECT '3XLARGE' AS WAREHOUSE_SIZE, 64 AS NODES 
            UNION ALL SELECT '4XLARGE' AS WAREHOUSE_SIZE, 128 AS NODES ) ), 
            QUERY_HISTORY AS ( 
                SELECT 
                QH.QUERY_ID , 
                QH.QUERY_TEXT , 
                QH.USER_NAME , 
                QH.ROLE_NAME ,
                QH.EXECUTION_TIME , 
                QH.WAREHOUSE_SIZE  
                FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY QH 
            WHERE START_TIME > DATEADD(month,-2,CURRENT_TIMESTAMP()) ) 
            SELECT 
                CAST((QH.EXECUTION_TIME/(1000)) AS FLOAT) as EXECUTION_TIME_SECONDS,
                QH.QUERY_TEXT ,
                QH.USER_NAME ,
                QH.ROLE_NAME ,
                sc.WAREHOUSE_SIZE ,sc.NODES ,    
                QH.QUERY_ID ,'https://' || current_account() || '.snowflakecomputing.com/console#/monitoring/queries/detail?queryId='||QH.QUERY_ID AS QU ,
                CAST((QH.EXECUTION_TIME/(1000*60*60))*sc.NODES AS FLOAT) as RELATIVE_PERFORMANCE_COST,
                QH.EXECUTION_TIME as EXECUTION_TIME_MILLISECONDS ,
                CAST((QH.EXECUTION_TIME/(1000*60))AS FLOAT) AS EXECUTION_TIME_MINUTES ,
                CAST((QH.EXECUTION_TIME/(1000*60*60)) AS FLOAT) AS EXECUTION_TIME_HOURS 
            FROM QUERY_HISTORY QH JOIN WAREHOUSE_SIZE sc 
            ON sc.WAREHOUSE_SIZE = upper(QH.WAREHOUSE_SIZE) 
            ORDER BY RELATIVE_PERFORMANCE_COST DESC LIMIT 200'''
    subhead1 = '過去30日間での高額なクエリ一覧'
    info = '過去30日間での高額なクエリはありません'
    disptype = 'dataframe'
    dispResult(cs, sql, col, info, disptype, subhead1)

# 自動クラスタリングと過去 30 日間にサービス経由で消費されたクレジット一覧
@print_log
def exeFunc44(cs):
    col = ['DATE', 'DATABASE_NAME', 'SCHEMA_NAME', 'TABLE_NAME', 'CREDITS_USED']
    sql = '''SELECT 
            TO_DATE(START_TIME) AS DATE ,
            DATABASE_NAME ,
            SCHEMA_NAME ,
            TABLE_NAME ,
            CAST(SUM(CREDITS_USED) AS FLOAT) AS CREDITS_USED 
        FROM "SNOWFLAKE"."ACCOUNT_USAGE"."AUTOMATIC_CLUSTERING_HISTORY" 
        WHERE START_TIME >= DATEADD(MONTH,-1,CURRENT_TIMESTAMP())  GROUP BY 1,2,3,4 ORDER BY 5 DESC'''
    subhead1 = '自動クラスタリングと過去 30 日間にサービス経由で消費されたクレジット一覧'
    info = '自動クラスタリングと過去 30 日間にサービス経由で消費されたクレジットはありません'
    disptype = 'dataframe'
    dispResult(cs, sql, col, info, disptype, subhead1)

# ウェアハウスごとのクエリあたりの平均コスト一覧（過去１か月）
@print_log
def exeFunc45(cs):
    col = ['WAREHOUSE_NAME', 'QUERY_COUNT_LAST_MONTH', 'CREDITS_USED_LAST_MONTH', 'CREDIT_COST_LAST_MONTH', 'COST_PER_QUERY']
    sql = '''SELECT 
            COALESCE(WC.WAREHOUSE_NAME,QC.WAREHOUSE_NAME) AS WAREHOUSE_NAME ,
            QC.QUERY_COUNT_LAST_MONTH ,WC.CREDITS_USED_LAST_MONTH ,
            WC.CREDIT_COST_LAST_MONTH
            ,CAST((WC.CREDIT_COST_LAST_MONTH / QC.QUERY_COUNT_LAST_MONTH) AS FLOAT ) AS COST_PER_QUERY 
        FROM ( SELECT WAREHOUSE_NAME ,COUNT(QUERY_ID) AS QUERY_COUNT_LAST_MONTH 
        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY WHERE TO_DATE(START_TIME) >= TO_DATE(DATEADD(MONTH,-1,CURRENT_TIMESTAMP())) GROUP BY WAREHOUSE_NAME ) 
        QC JOIN ( 
        SELECT 
            WAREHOUSE_NAME ,
            CAST(SUM(CREDITS_USED) AS FLOAT) AS CREDITS_USED_LAST_MONTH ,
            CAST(SUM(CREDITS_USED)*($CREDIT_PRICE) AS FLOAT) AS CREDIT_COST_LAST_MONTH 
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY WHERE TO_DATE(START_TIME) >= TO_DATE(DATEADD(MONTH,-1,CURRENT_TIMESTAMP())) 
        GROUP BY WAREHOUSE_NAME ) WC ON WC.WAREHOUSE_NAME = QC.WAREHOUSE_NAME ORDER BY COST_PER_QUERY DESC'''
    subhead1 = 'ウェアハウスごとのクエリあたりの平均コスト一覧（過去１か月）'
    disptype = 'dataframe'
    info = '過去１か月にクエリは実行されていません'
    cs.execute("SET CREDIT_PRICE = 4")
    dispResult(cs, sql, col, info, disptype, subhead1)