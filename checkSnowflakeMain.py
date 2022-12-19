##**************************************************************************
## システム名   :Snowflake ウェアハウス監視ツール
## 業務名   :NTTD_Snowflake支援業務
##-------------------------------------------------------------------------
## 更新履歴
##  2022.07.25  益田理菜  初版
##  XXXX.XX.XX  XX XX  インシデントNO:00000  XXX対応
##*************************************************************************

##################################################
# モジュールインポート 
##################################################
import snowflake.connector
import streamlit as st
from PIL import Image
import configparser
from Utils import *
from dispResult import *

##################################################
# パラメーター設定 
##################################################
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
 
##################################################
# 変数設定
##################################################
snow_image = config_ini['COMMON']['SNOW_IMAGE']

##################################################
# タイトル設定
##################################################
st.set_page_config(
     page_title="Snowflake_CheckWarehousesTool",
 )

##################################################
# 関数
##################################################

###################################################
# 関数名：main
#
# 機能概要：
# １ページ目の表示
##################################################
@print_log
def main():
	# １ページ目表示
    # st.subheader("Snowflake ウェアハウス監視ツール")
    with st.form("my_form"):
        image = Image.open(snow_image)
        col1, col2, col3 = st.columns([1.5, 1, 1])
        with col1:
            st.write('')
        with col2:
            st.image(image, use_column_width=False)
        with col3:
            st.write('')

        col1, col2, col3 = st.columns([0.07, 1, 0.1])
        with col1:
            st.write('')
        with col2:
            st.header("Snowflake ウェアハウス監視ツール")  
        with col3:
            st.write('')

        col1, col2, col3 = st.columns([0.12, 1, 0.1])
        with col1:
            st.write('')
        with col2:
            st.subheader("Snowflakeの認証情報を入力してください")  
        with col3:
            st.write('')
 
        st.text_input("アカウント識別子 (必須) ",  placeholder="例: ht88761.ap-northeast-1.aws", key="アカウント名", help=' Snowflake環境のアカウント識別子(※)を記載してください。  \n  ※ログインURLの<アカウント識別子>部分  \n  https://<アカウント識別子>.snowflakecomputing.com')
        st.text_input("ユーザー名 (必須)",  placeholder="例: SNOWFLAKE_USER", key="ユーザー名", help='Snowflakeログイン時のユーザー名を入力してください')
        st.text_input("パスワード (必須)",  key="パスワード", type='password')
        st.text_input("ロール",  placeholder="例: ACCOUNTADMIN", key="ロール", help='ユーザーにデフォルトのロールが設定されていない場合は、  \n  使用するロールを記入してください')
        st.text_input("ウェアハウス", placeholder="例: COMPUTE_WH", key="ウェアハウス", help='ユーザーにデフォルトのウェアハウスが設定されていない場合は、  \n  使用するウェアハウスを記入してください ') 

        col1, col2, col3 = st.columns([1.5, 1, 1])
        with col1:
            st.write('')
        with col2:
            st.form_submit_button("OK", on_click=changePage)
        with col3:
            st.write('')

###################################################
# 関数名：mainforBack
#
# 機能概要：
# 認証情報変更の際のページ
##################################################
@print_log
def mainforBack():
	# １ページ目表示
    with st.form("my_form"):
        image = Image.open(snow_image)
        col1, col2, col3 = st.columns([1.5, 1, 1])
        with col1:
            st.write('')
        with col2:
            st.image(image, use_column_width=False)
        with col3:
            st.write('')

        col1, col2, col3 = st.columns([0.07, 1, 0.1])
        with col1:
            st.write('')
        with col2:
            st.header("Snowflake ウェアハウス監視ツール")  
        with col3:
            st.write('')

        col1, col2, col3 = st.columns([0.12, 1, 0.1])
        with col1:
            st.write('')
        with col2:
            st.subheader("Snowflakeの認証情報を入力してください")  
        with col3:
            st.write('')
        
        # 認証情報入力画面
        st.text_input("アカウント名 (必須) ", value = st.session_state["アカウント名"], placeholder="例: ht88761.ap-northeast-1.aws", key="アカウント名", help=' Snowflake環境のアカウント識別子(※)を記載してください。  \n  ※ログインURLの<アカウント識別子>部分  \n  https://<アカウント識別子>.snowflakecomputing.com')

        st.text_input("ユーザー名 (必須)", value = st.session_state["ユーザー名"], placeholder="例: SNOWFLAKE_USER", key="ユーザー名", help='Snowflakeログイン時のユーザー名を入力してください')
        
        st.text_input("パスワード (必須)", value = st.session_state["パスワード"], key="パスワード", type='password')

        if st.session_state["ロール"]:
            st.text_input("ロール", value = st.session_state["ロール"], placeholder="例: ACCOUNTADMIN", key="ロール", help='ユーザーにデフォルトのロールが設定されていない場合は、  \n  使用するロールを記入してください')
        else:
            st.text_input("ロール", placeholder="例: ACCOUNTADMIN", key="ロール", help='ユーザーにデフォルトのロールが設定されていない場合は、  \n  使用するロールを記入してください')
        
        if st.session_state["ウェアハウス"]:
            st.text_input("ウェアハウス", value = st.session_state["ウェアハウス"],  placeholder="例: COMPUTE_WH", key="ウェアハウス", help='ユーザーにデフォルトのウェアハウスが設定されていない場合は、  \n  使用するウェアハウスを記入してください') 
        else:
            st.text_input("ウェアハウス", placeholder="例: COMPUTE_WH", key="ウェアハウス", help='ユーザーにデフォルトのウェアハウスが設定されていない場合は、  \n  使用するウェアハウスを記入してください') 

        col1, col2, col3 = st.columns([1.5, 1, 1])
        with col1:
            st.write('')
        with col2:
            st.form_submit_button("OK", on_click=changePage)
        with col3:
            st.write('')

###################################################
# 関数名：nextPage
#
# 機能概要：
# ２ページ目の内容を表示する
##################################################
@print_log
def nextPage():

    # 1ページ目の変数を代入
    sf_user = st.session_state["ユーザー名"]
    sf_password = st.session_state["パスワード"]
    sf_account = st.session_state["アカウント名"]
    sf_role = st.session_state["ロール"]
    sf_warehouse = st.session_state["ウェアハウス"]

    try:
        # 変数代入
        ctx = snowflake.connector.connect(
        user=sf_user,
        password=sf_password,
        account=sf_account,
        )
        cs = ctx.cursor()

    except snowflake.connector.errors.DatabaseError:
        st.error("アカウント名、ユーザー名、パスワードのいずれかが間違っています")
        mainforBack()

    else:
        #　ロール指定
        if sf_role:
            cs.execute("use role " + sf_role)

        # ウェアハウス指定
        if sf_warehouse:
            cs.execute("use warehouse " + sf_warehouse)

        # サイドバー移動の際の変数保持
        if "ユーザー名 "not in st.session_state:
            st.session_state["ユーザー名"] = sf_user
        if "パスワード "not in st.session_state:
            st.session_state["パスワード"] = sf_password
        if "アカウント名 "not in st.session_state:
            st.session_state["アカウント名"] = sf_account
        if "ロール "not in st.session_state:
            st.session_state["ロール"] = sf_role
        if "ウェアハウス "not in st.session_state:
            st.session_state["ウェアハウス"] = sf_warehouse

        # ユーザー名、ロールを表示
        # st.set_page_config(layout="wide")
        st.title('Snowflake ウェアハウス監視ツール')
        st.sidebar.caption("ユーザー名")
        st.sidebar.caption(sf_user)
        if sf_role:
            st.sidebar.caption("ロール")
            st.sidebar.caption(sf_role)
        else:
            sf_current_role = cs.execute("select current_role()").fetchall()
            st1 = str(sf_current_role)[3:]
            sf_role = st1[:-4]
            st.sidebar.caption("ロール")
            st.sidebar.caption(sf_role)

        # プルダウンリストの作成
        st.sidebar.write(" ")
        st.sidebar.write(" ")
        st.sidebar.write(" ")
        st.sidebar.write(" ")
        pagelist = ["セットアップ・構成の確認", "利用状況確認", "パフォーマンス状況確認" , "コスト確認"]
        selector = st.sidebar.selectbox( "<確認項目を選択してください>",pagelist)
        st.sidebar.write(" ")

        if selector=="セットアップ・構成の確認":

            pagelist_setup = ["すべて表示", "ウェアハウス一覧", "自動再開が有効になっているウェアハウス一覧", 
                            "自動サスペンドが有効になっているウェアハウス一覧", "自動停止時間が1分より長いウェアハウス一覧", "過去３０日間にログインしていないユーザー一覧", 
                            "未ログインユーザー一覧", "ステートメントタイムアウトの設定", "過去７日間で失敗したタスク一覧", "過去７日間で長時間実行されたタスク一覧"]
            selector_setup = st.sidebar.selectbox( "  <表示したい項目を選択してください>",pagelist_setup)

            if selector_setup == "すべて表示":
                exeFunc11(cs)
                exeFunc12(cs)
                exeFunc14(cs)
                exeFunc15(cs)
                exeFunc16(cs)
                exeFunc17(cs, sf_user, sf_warehouse)
                exeFunc18(cs)
                exeFunc19(cs)

            if selector_setup == "ウェアハウス一覧":
                exeFunc11(cs)

            if selector_setup == "自動再開が有効になっているウェアハウス一覧":
                exeFunc12(cs)

            if selector_setup == "自動サスペンドが有効になっているウェアハウス一覧":
                exeFunc13(cs)

            if selector_setup == "自動停止時間が1分より長いウェアハウス一覧":
                exeFunc14(cs)

            if selector_setup == "過去３０日間にログインしていないユーザー一覧":
                exeFunc15(cs)

            if selector_setup == "未ログインユーザー一覧":
                exeFunc16(cs)

            if selector_setup == "ステートメントタイムアウトの設定":
                exeFunc17(cs, sf_user, sf_warehouse)
            
            if selector_setup == "過去７日間で失敗したタスク一覧":
                exeFunc18(cs)
            
            if selector_setup == "過去７日間で長時間実行されたタスク一覧":
                exeFunc19(cs)

        elif selector=="利用状況確認":

            pagelist_usage = ["すべて表示", "ウェアハウス別のクレジット使用", "１時間ごとのウェアハウス別のクレジット使用（過去７日間）", 
                            "１時間ごとのクエリ数（過去７日間）", "過去１年間の数週間にわたるウェアハウスのクレジット消費の異常を特定"]
            selector_usage = st.sidebar.selectbox( "<表示したい項目を選択してください>",pagelist_usage)

            if selector_usage == "すべて表示":
                exeFunc21(cs)
                exeFunc22(cs)
                exeFunc23(cs)
                exeFunc24(cs)

            if selector_usage == "ウェアハウス別のクレジット使用":
                exeFunc21(cs)

            if selector_usage == "１時間ごとのウェアハウス別のクレジット使用（過去７日間）":
                exeFunc22(cs)

            if selector_usage == "１時間ごとのクエリ数（過去７日間）":
                exeFunc23(cs)

            if selector_usage == "過去１年間の数週間にわたるウェアハウスのクレジット消費の異常を特定":
                exeFunc24(cs)

        elif selector=="パフォーマンス状況確認":

            pagelist_performance = ["すべて表示", "大量のデータをスキャンするクエリを実行しているユーザー一覧（過去４５日間）", 
                                    "リモートストレージに流出したバイト数の観点から、問題のあるクエリ一覧（過去４５日間 / 上位１０件のクエリ）", 
                                    "過去 1 年間に自動クラスタリングによって消費された 1 日の平均クレジットの一覧", "マテリアライズドビューが過去１年間に消費した１日の平均クレジットの一覧", 
                                    "過去１年間の検索最適化サービス(SOS)履歴と7日間平均の一覧", "Snowpipe が過去 1 年間に消費した 1 日の平均クレジットの一覧"]
            selector_performance = st.sidebar.selectbox( "<表示したい項目を選択してください>",pagelist_performance)

            if selector_performance == "すべて表示":
                exeFunc31(cs)
                exeFunc32(cs)
                exeFunc33(cs)
                exeFunc34(cs)
                exeFunc35(cs)
                exeFunc36(cs)

            if selector_performance == "大量のデータをスキャンするクエリを実行しているユーザー一覧（過去４５日間）":
                exeFunc31(cs)

            if selector_performance == "リモートストレージに流出したバイト数の観点から、問題のあるクエリ一覧（過去４５日間 / 上位１０件のクエリ）":
                exeFunc32(cs)

            if selector_performance == "過去 1 年間に自動クラスタリングによって消費された 1 日の平均クレジットの一覧":
                exeFunc33(cs)

            if selector_performance == "マテリアライズドビューが過去１年間に消費した１日の平均クレジットの一覧":
                exeFunc34(cs)

            if selector_performance == "過去１年間の検索最適化サービス(SOS)履歴と7日間平均の一覧":
                exeFunc35(cs)

            if selector_performance == "Snowpipe が過去 1 年間に消費した 1 日の平均クレジットの一覧":
                exeFunc36(cs)

        elif selector=="コスト確認":
            pagelist_cost = ["すべて表示", "日付ごとのタイプ別利用一覧", "期間ごとのウェアハウス別クレジット一覧", "過去30日間での高額なクエリ一覧", "自動クラスタリングと過去 30 日間にサービス経由で消費されたクレジット一覧",
                            "ウェアハウスごとのクエリあたりの平均コスト一覧（過去１か月）"]
            selector_cost = st.sidebar.selectbox( "<表示したい項目を選択してください>",pagelist_cost)

            if selector_cost == "すべて表示":
                exeFunc41(cs)
                exeFunc42(cs)
                exeFunc43(cs)
                exeFunc44(cs)
                exeFunc45(cs)

            if selector_cost == "日付ごとのタイプ別利用一覧":
                exeFunc41(cs)

            if selector_cost == "期間ごとのウェアハウス別クレジット一覧":
                exeFunc42(cs)

            if selector_cost == "過去30日間での高額なクエリ一覧":
                exeFunc43(cs)

            if selector_cost == "自動クラスタリングと過去 30 日間にサービス経由で消費されたクレジット一覧":
                exeFunc44(cs)

            if selector_cost == "ウェアハウスごとのクエリあたりの平均コスト一覧（過去１か月）":
                exeFunc45(cs)

        # 空白追加
        st.sidebar.write(" ")
        st.sidebar.write(" ") 
        st.sidebar.write(" ") 
        st.sidebar.write(" ") 
        st.sidebar.write(" ")  
        st.sidebar.write(" ") 
        st.sidebar.write(" ") 

        # アカウント名表示
        image = Image.open(snow_image)
        st.sidebar.image(image, use_column_width=False)
        st.sidebar.caption("アカウント名")
        st.sidebar.caption(sf_account)

        st.sidebar.write(" ") 

        # トップ画面に戻るボタンの作成
        st.sidebar.button('''アカウントを切り替える''', on_click=toPrevPage, help = "ユーザー名、ロール、アカウントを変更する")

###################################################
# 関数名：changePage
#
# 機能概要：
# 認証情報２ページ目に移動する
##################################################
@print_log
def changePage():    
    # 2ページ目に移動
    if not st.session_state["アカウント名"]:
        st.session_state["page_control"]=0
        st.error("アカウント名を入力してください")
        
    elif not st.session_state["ユーザー名"]:
        st.session_state["page_control"]=0
        st.error("ユーザー名を入力してください")

    elif not st.session_state["パスワード"]:
        st.session_state["page_control"]=0
        st.error("パスワードを入力してください")

    else:
        st.session_state["page_control"]=1

###################################################
# 関数名：toPrevPage
#
# 機能概要：nextPage
# トップ画面に戻る
##################################################
@print_log
def toPrevPage():
    # ページ移動処理    
    # global sf_account
    st.session_state["page_control"]=2

##################################################
# ツール実行
##################################################

if ("page_control" in st.session_state and
st.session_state["page_control"] == 1):
    nextPage()
elif ("page_control" in st.session_state and
st.session_state["page_control"] == 2):
    mainforBack()
else:
    st.session_state["page_control"] = 0
    main()