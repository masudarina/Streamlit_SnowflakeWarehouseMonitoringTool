##**************************************************************************
## システム名	:データカタログ
## 業務名	:NTTD_Snowflake支援業務
##-------------------------------------------------------------------------
## 更新履歴
##	2022.12.19	益田理菜  初版
##	XXXX.XX.XX	XX XX  インシデントNO:00000	 XXX対応
##*************************************************************************

##################################################
# モジュールインポート 
##################################################
import streamlit as st
import pandas as pd
import snowflake.connector
import streamlit.components.v1 as components
import os
from PIL import Image

##################################################
# パラメーター設定 
##################################################
current_path = os.path.dirname(os.path.abspath(__file__))
basename_without_ext = os.path.splitext(os.path.basename(os.path.basename(__file__)))[0]
snow_image = os.path.join(current_path, 'Snowflake.png')

##################################################
# 変数設定
##################################################
# ページ設定
st.set_page_config(
	page_title=basename_without_ext,
	page_icon="❄"
	, layout="wide"
)

##################################################
# CSS, HTML設定
##################################################
# ボタン
button_css = f"""
<style>
div.stButton > button:first-child  {{
	color		 : #ffffff				 ;
	background	 : #00A1FF			   ;
}}
</style>
"""

# テーブルのindex表示の削除
# 注：インデントなし(左揃え)にする必要あり
hide_dataframe_row_index = """
<style>
.row_heading.level0 {display:none}
.blank {display:none}
</style>
"""

# CSS適用
st.markdown(button_css, unsafe_allow_html=True)
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

##################################################
# 関数　
##################################################

###################################################
# 関数名：makeDataframe
#
# 機能概要：
# データフレームの作成、連番設定
##################################################
def makeDataframe(data, columns):

	# データフレーム作成
	st.session_state["df_table"] = pd.DataFrame(data, columns=columns)

###################################################
# 関数名：prerareSelectbox
#
# 機能概要：
# セレクトボックスの選択肢を作成
##################################################
def prerareSelectbox():

	# 型をpandasSeriesに変換
	selected_area2 = st.session_state["df_table"]["テーブル名"]

	# listに変換
	st.session_state["my_list3"] = list(selected_area2)

###################################################
# 関数名：returnPrevPage
#
# 機能概要：nextPage
# トップ画面に戻る
##################################################
def returnPrevPage():

	# ページ移動処理	
	st.session_state["page_control"]=2

###################################################
# 関数名：changePage
#
# 機能概要：
# 認証情報２ページ目に移動する
##################################################
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
# 関数名：showTables
#
# 機能概要：
# スキーマ情報からテーブル情報を取得
##################################################
def showTables(cs):

	# データベース名、スキーマ名に合致するテーブル情報を取得
	st.session_state["table_result"] = cs.execute('''SHOW TERSE TABLES IN ''' + str(st.session_state["データベース選択"]) + '''.''' + str(st.session_state["スキーマ名"]))

###################################################
# 関数名：searchTables
#
# 機能概要：
# テーブル情報検索結果からデータ取得
##################################################
def searchTables(cs):

	# データベース名、スキーマ名に合致するテーブル情報を取得
	cs.execute('''SHOW TABLES IN ''' + st.session_state["データベース選択"] + '''.''' + st.session_state["スキーマ名"]) 

	# 検索
	st.session_state['table_search_result'] = cs.execute('''
		SELECT 
				"name"
		FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
		WHERE UPPER("name") LIKE \'%''' + st.session_state["search_table"].upper() + '''%\'''' + '''
		AND "database_name" = \'''' + st.session_state["データベース名"] + '''\' 
		AND "schema_name" = \'''' + st.session_state["スキーマ名"] + '''\'
		''').fetchall()
	
###################################################
# 関数名：searchColumns
#
# 機能概要：
# カラム情報検索結果からデータ取得
##################################################
def searchColumns(cs):

	# データベース名、スキーマ名に合致するテーブル情報を取得
	cs.execute('''SHOW COLUMNS IN SCHEMA ''' + st.session_state["データベース選択"] + '''.''' + st.session_state["スキーマ名"])

	# 検索
	st.session_state['columns_search_result'] = cs.execute('''
		SELECT 
			"table_name"
		FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
		WHERE UPPER("column_name") LIKE \'%''' + st.session_state["search_column"].upper() + '''%\'''' + '''
		AND "database_name" = \'''' + st.session_state["データベース名"] + '''\'''' + '''
		AND "kind" = 'COLUMN\' 
		AND "schema_name" = \'''' + st.session_state["スキーマ名"] + '''\'
		''').fetchall()

###################################################
# 関数名：disploginPage
#
# 機能概要：
# １ページ目（ログイン画面）の表示
##################################################
def disploginPage():
	
	# 画面分割
	col1, col2, col3 = st.columns([0.9, 1, 0.9])

	with col1:
		st.write('')

	with col2:
		with st.form("my_form"):
			# htmlで表示を中心に寄せる
			header = "<h1>データカタログ</h1><h4>Snowflakeの認証情報を入力してください </h4>"
			st.components.v1.html("<center>" + header + "</center>") 
			st.text_input("アカウント識別子 (必須) ",  placeholder="例: ht88761.ap-northeast-1.aws", key="アカウント名", help=' Snowflake環境のアカウント識別子(※)を記載してください。	 \n	 ※ログインURLの<アカウント識別子>部分	\n	https://<アカウント識別子>.snowflakecomputing.com')
			st.text_input("ユーザー名 (必須)",	placeholder="例: SNOWFLAKE_USER", key="ユーザー名", help='Snowflakeログイン時のユーザー名を入力してください')
			st.text_input("パスワード (必須)",	key="パスワード", type='password')
			st.text_input("ロール",	 placeholder="例: ACCOUNTADMIN", key="ロール", help='ユーザーにデフォルトのロールが設定されていない場合は、	 \n	 使用するロールを記入してください')
			st.text_input("ウェアハウス", placeholder="例: COMPUTE_WH", key="ウェアハウス", help='ユーザーにデフォルトのウェアハウスが設定されていない場合は、	\n	使用するウェアハウスを記入してください ') 
			st.form_submit_button("OK", on_click=changePage)

		with col3:
			st.write('')

###################################################
# 関数名：disploginPageforBack
#
# 機能概要：
# 認証情報変更の際のページ
##################################################
def disploginPageforBack():

	# 画面分割
	col1, col2, col3 = st.columns([0.9, 1, 0.9])

	with col1:
		st.write('')

	with col2:
		with st.form("my_form"):
			# htmlで表示を中心に寄せる
			header = "<h1>データカタログ</h1><h4>Snowflakeの認証情報を入力してください </h4>"
			st.components.v1.html("<center>" + header + "</center>") 
			st.text_input("アカウント名 (必須) ",  value = st.session_state["アカウント名"], placeholder="例: ht88761.ap-northeast-1.aws", key="アカウント名", help=' Snowflake環境のアカウント識別子(※)を記載してください。  \n  ※ログインURLの<アカウント識別子>部分  \n  https://<アカウント識別子>.snowflakecomputing.com')

			st.text_input("ユーザー名 (必須)", value = st.session_state["ユーザー名"], placeholder="例: SNOWFLAKE_USER", key="ユーザー名", help='Snowflakeログイン時のユーザー名を入力してください')
			
			st.text_input("パスワード (必須)", value = st.session_state["パスワード"], key="パスワード", type='password')

			if st.session_state["ロール"]:
				st.text_input("ロール", value = st.session_state["ロール"], placeholder="例: ACCOUNTADMIN", key="ロール", help='ユーザーにデフォルトのロールが設定されていない場合は、	\n	使用するロールを記入してください')
			else:
				st.text_input("ロール", placeholder="例: ACCOUNTADMIN", key="ロール", help='ユーザーにデフォルトのロールが設定されていない場合は、	\n	使用するロールを記入してください')
			
			if st.session_state["ウェアハウス"]:
				st.text_input("ウェアハウス", value = st.session_state["ウェアハウス"],	 placeholder="例: COMPUTE_WH", key="ウェアハウス", help='ユーザーにデフォルトのウェアハウスが設定されていない場合は、  \n  使用するウェアハウスを記入してください') 
			else:
				st.text_input("ウェアハウス", placeholder="例: COMPUTE_WH", key="ウェアハウス", help='ユーザーにデフォルトのウェアハウスが設定されていない場合は、	\n	使用するウェアハウスを記入してください')			 
			st.form_submit_button("OK", on_click=changePage)

		with col3:
			st.write('')

###################################################
# 関数名：dispdispMainPageDetailTableInfo
#
# 機能概要：
# テーブル基本情報表示
##################################################
def dispdispMainPageDetailTableInfo(cs):

	# タイトル表示(例：テーブル詳細 選択中： テーブル名)
	st.write('<span style="font-size: 20px;">テーブル詳細 選択中：</span>', \
			'''<span style="color:#000000; font-size: 20px; font-weight : bold;">''' \
			+ st.session_state["テーブル名"] + '''</span>''', \
			unsafe_allow_html=True)

	# テーブル一覧取得
	cs.execute('''SHOW TABLES LIKE ''' + '''\'''' + st.session_state["テーブル名"] \
		+ '''\' IN SCHEMA ''' + st.session_state["データベース選択"] + '''.''' + st.session_state["スキーマ名"])

	# テーブル情報取得
	tableinfo_result = cs.execute('''
		SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) \
		WHERE "name" = ''' + '''\'''' + st.session_state["テーブル名"] + '''\'''')

	# テーブル情報をDataframeに代入
	df_tableinfo = pd.DataFrame(tableinfo_result, 
		columns = ["作成日時", "テーブル名", "データベース" ,"スキーマ" ,"種類" ,"コメント" ,"cluster_by" ,\
			"レコード数" ,"データ量（bytes）" ,"所有者" ,"データ保持期間(日)" ,"自動クラスタリング" ,\
			"change_tracking" ,"search_optimization" ,"search_optimization_progress" ,\
			"search_optimization_bytes", "is_external"])

	# 画面への表示順を並び替え
	df_tableinfo = df_tableinfo[["テーブル名","データベース","スキーマ","所有者","レコード数",\
		"データ量（bytes）","作成日時","コメント","データ保持期間(日)","自動クラスタリング", \
		"cluster_by" ,"change_tracking" ,"search_optimization" ,"search_optimization_progress" ,\
		"search_optimization_bytes", "is_external"]]

	# 作成日時カラムの形式変換
	df_tableinfo['作成日時'] = pd.to_datetime(df_tableinfo['作成日時'])
	df_tableinfo['作成日時'] = df_tableinfo['作成日時'].dt.strftime('%Y-%m-%d %H:%M:%S')

	# テーブル表示
	st.table(df_tableinfo.T.reset_index().rename(columns={"index":"項目", 0:"設定値"}).style.set_table_styles(
		[{"selector": "th", "props": [("background-color", "#f0f8ff"), ("color", "black"), \
		("font-weight", "bold"), ("text-align", "center")]}]
	))

###################################################
# 関数名：dispdispMainPageDetailColumns
#
# 機能概要：
# カラム一覧取得
##################################################
def dispdispMainPageDetailColumns(cs):

	#  カラムデータ取得
	columns_result = cs.execute('''SHOW TERSE COLUMNS IN TABLE '''\
			+ st.session_state["データベース選択"] + '''.'''\
			+ st.session_state["スキーマ名"] + '''.''' + st.session_state["テーブル名"])

	# カラム情報をDataframeに代入
	df_columns = pd.DataFrame(columns_result, \
		columns = ["table_name", "schema_name", "カラム名", "data_type",\
				"null?", "default", "kind", "expression", "comment", "database_name", "autoincrement"])

	# カラム名指定
	st.session_state["df_columns"] = df_columns["カラム名"]

	# 連番を1から開始
	st.session_state["df_columns"].index = st.session_state["df_columns"].index + 1

###################################################
# 関数名：dispdispMainPageDetailColumnsList
#
# 機能概要：
# カラム詳細情報取得
##################################################
def dispdispMainPageDetailColumnsList(cs):

	# カラム詳細情報取得
	cs.execute('''USE ''' + '''"''' + st.session_state["データベース名"] + '''".'''\
			+ '''"''' + st.session_state["スキーマ名"] + '''"''')

	cs.execute('''DESC TABLE ''' + st.session_state["テーブル名"])

	columns_details1 = cs.execute('''
		SELECT 
			"name",
			"type",
			"kind",
			"null?",
			"default",
			"primary key",
			"unique key",
			"comment",
			"policy name"
		FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
		WHERE "name" = \'''' + st.session_state["selected_area3"] + '''\'
	''').fetchall()

	# テーブル情報をDataframeに代入
	df_columns1 = pd.DataFrame(columns_details1, \
		columns = ["カラム名","データ型","種類","nullの可否","デフォルト",\
			"プライマリーキー","ユニークキー", "コメント","ポリシー名"])	

	try:
		# レコード数、最大値、最小値を取得
		columns_details2 = cs.execute('''
			SELECT 
				COUNT(''' + st.session_state["selected_area3"] + '''),
				MAX(''' + st.session_state["selected_area3"] + '''),
				MIN(''' + st.session_state["selected_area3"] + '''), 
				(SELECT 
					COUNT(*) 
				FROM '''  + st.session_state["テーブル名"] + ''' 
				WHERE ''' + st.session_state["selected_area3"] + ''' is NULL) AS "count(null)" 
			FROM '''  + st.session_state["テーブル名"] 
				).fetchall()

		# テーブル情報をDataframeに代入
		df_columns2 = pd.DataFrame(columns_details2, columns = ["カウント数","最大値","最小値", "nullの数"])

		# データフレーム結合
		df_columns3 = pd.concat([df_columns1, df_columns2], axis=1)

		# 表示順指定
		st.session_state["df_columns4"] = df_columns3[["カラム名", "データ型", "カウント数","最大値","最小値",\
				"nullの可否", "nullの数", "種類","デフォルト","プライマリーキー","ユニークキー",\
				"ポリシー名", "コメント"]]
 
	# 地理空間型を選択した際に最大値、最小値が検出されずエラーになるため回避
	except snowflake.connector.errors.ProgrammingError: 
	
		# レコード数、空白数を取得
		columns_details2 = cs.execute('''
			SELECT 
				COUNT(''' + st.session_state["selected_area3"] + '''), 
				(SELECT 
					COUNT(*) 
					FROM '''  + st.session_state["テーブル名"] +
					''' WHERE ''' + st.session_state["selected_area3"] + ''' is NULL) AS "count(null)" 
				FROM '''  + st.session_state["テーブル名"] 
			 ).fetchall()

		# テーブル情報をDataframeに代入
		df_columns2 = pd.DataFrame(columns_details2, columns = ["カウント数", "nullの数"])

		# データフレーム結合
		df_columns3 = pd.concat([df_columns1, df_columns2], axis=1)

		# 表示順指定
		st.session_state["df_columns4"] = df_columns3[["カラム名", "データ型", "カウント数", "nullの可否", "nullの数",\
				"種類","デフォルト","プライマリーキー","ユニークキー","ポリシー名", "コメント"]]

###################################################
# 関数名：dispdispMainPageDetailColumnInfo

# 機能概要：
# カラム詳細情報表示
##################################################
def dispdispMainPageDetailColumnInfo(cs):

	# 画面分割
	col1, col2 = st.columns([1, 1])
	with col1:
		# カラム一覧作成
		st.write("カラム一覧")
		st.dataframe(st.session_state["df_columns"],600)

	with col2:
		# セレクトボックスを作成 リスト選択時は再描画の挙動
		area_list3 = st.session_state["df_columns"]
		st.session_state["selected_area3"] = st.selectbox(
			'カラム選択',
			area_list3
		, on_change=dispMainPage
		)

		# カラム詳細情報取得
		dispdispMainPageDetailColumnsList(cs)

		# 選択表示
		st.write('<span style="font-size: 20px;">カラム詳細 選択中：</span>',\
			'''<span style="color:#000000; font-size: 20px; font-weight : bold;">'''\
			+ st.session_state["selected_area3"] + '''</span>'''\
			,unsafe_allow_html=True) 
		
		# 詳細情報表示
		st.table(st.session_state["df_columns4"].T.reset_index().rename(columns={"index":"項目", 0:"設定値"}).style.set_table_styles(
			[{"selector": "th", "props": [("background-color", "#f0f8ff"), ("color", "black"), \
			("font-weight", "bold"), ("text-align", "center")]}]
		))

###################################################
# 関数名：dispSideDatabaseList
#
# 機能概要：
# データベースの一覧を取得
##################################################
def dispSideDatabaseList(cs):

    # データベース情報取得
    db_result = cs.execute("SHOW TERSE DATABASES")

    # テーブル情報をDataframeに代入 
    df_db = pd.DataFrame(db_result, columns = ["created_on", "データベース名", "kind", "database_name", "schema_name"])

    # データベース名のカラムをリストに代入
    st.session_state["area_list1"] = df_db['データベース名'].unique()

    # st.write(st.session_state["area_list1"])
 
###################################################
# 関数名：dispSideSchemaList
#
# 機能概要：
# スキーマ情報を取得
##################################################
def dispSideSchemaList(cs):

	# データベース名に合致するテーブル情報を取得
	schema_result = cs.execute('''SHOW TERSE TABLES IN DATABASE ''' + st.session_state["データベース選択"])

	# テーブル情報をDataframeに代入 
	df_db = pd.DataFrame(schema_result, columns = ["created_on", "name", "kind", "database_name", "スキーマ名"])

	# データベース名のカラムをリストに代入
	st.session_state["area_list3"] = df_db['スキーマ名'].unique()

###################################################
# 関数名：dispSideTableList
#
# 機能概要：
# テーブル選択の作成
##################################################
def dispSideTableList(cs):

	# テーブル検索：あり　カラム検索：あり
	if st.session_state['search_table'] and st.session_state['search_column']:

		# テーブル情報取得　
		if searchTables(cs) == False:
			st.error("テーブル情報が取得できません")
			pass

		if  searchColumns(cs) == False:
			st.error("テーブル情報が取得できません")
			pass

		# データフレーム作成
		# list結合
		data = st.session_state['table_search_result'] + st.session_state['columns_search_result']
		columns=["テーブル名"]
		makeDataframe(data,columns)


	# テーブル検索：あり　カラム検索：なし
	elif st.session_state["search_table"] and not st.session_state["search_column"]:

		# テーブル情報取得　
		if searchTables(cs) == False:
			st.error("テーブル情報が取得できません")
			pass             

		# データフレーム作成
		data = st.session_state['table_search_result']
		columns=["テーブル名"]
		makeDataframe(data,columns)


    # テーブル検索：なし　カラム検索：あり
	elif not st.session_state["search_table"] and st.session_state["search_column"]:

		# テーブル情報取得　
		if searchColumns(cs) == False:
			st.error("テーブル情報が取得できません")
			pass

		# データフレーム作成
		data = list(st.session_state['columns_search_result'])
		columns=["テーブル名"]
		makeDataframe(data,columns)


	# テーブル検索：なし　カラム検索：なし
	elif not st.session_state["search_table"] and not st.session_state["search_column"]:

		# テーブル情報取得
		if showTables(cs) == False:
			st.error("テーブル情報が取得できません")
			pass
		
		# データフレーム作成　
		data = st.session_state["table_result"]
		columns=["created_on", "テーブル名", "kind", "database_name", "schema_name"]
		makeDataframe(data,columns)

		# カラム名をテーブル名だけに絞る
		st.session_state["df_table"] = st.session_state["df_table"][['テーブル名']]

	prerareSelectbox()

###################################################
# 関数名：dispMainPage　
#
# 機能概要：
# メイン画面作成
##################################################
def dispMainPage():
	
	# カーソル指定
	cs = st.session_state["cs"]

	st.title("データカタログ")

	if dispdispMainPageDetailTableInfo(cs) == False:
		st.error("テーブル基本情報表示を表示できません")
		pass 
	if dispdispMainPageDetailColumns(cs) == False:
		st.error("カラム詳細がありません")
		pass		 
	if dispdispMainPageDetailColumnInfo(cs) == False:
		st.error("テーブル基本情報表示を表示できません")
		pass 

###################################################
# 関数名：dispSidePage　
#
# 機能概要：
# メイン画面の表示
##################################################
def dispSidePage():

	# テキスト入力箇所 (インデント入れると認識されない為、以下変更不可)
	components.html("""
	<script>
	const elements = window.parent.document.querySelectorAll('.stTextInput div[data-baseweb="input"] > div')
	console.log(elements)
	elements[0].style.backgroundColor = '#f5f5f5',
	elements[1].style.backgroundColor = '#f5f5f5'
	</script>
	""",height=0,width=0
	) 

	# 1ページ目のSnowflake認証情報の変数を代入
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
		# カーソル作成
		cs = ctx.cursor()
		# csをセッションスステイトで保持（関数dispMainPageで使用）
		st.session_state["cs"] = cs

	# ログイン情報の確認
	except snowflake.connector.errors.DatabaseError:
		disploginPageforBack()
		col1, col2, col3 = st.columns([0.9, 1, 0.9])
		with col1:
			st.write(" ")
		with col2:
			st.error("アカウント名、ユーザー名、パスワードのいずれかが間違っています。")
		with col3:
			st.write(" ")

	else:
		try:
			# ロール指定
			if sf_role:
				cs.execute("use role " + sf_role)

			# ウェアハウス指定
			if sf_warehouse:
					cs.execute("use warehouse " + sf_warehouse)

		# ロール、ウェハウスの権限を確認
		except snowflake.connector.errors.ProgrammingError:
			disploginPageforBack()
			col1, col2, col3 = st.columns([0.9, 1, 0.9])
			with col1:
				st.write(" ")
			with col2:
				st.error("現在ログインしているユーザーでは指定したロールまたはウェアハウスを使用することができません。権限を確認してください。")
			with col3:
				st.write(" ")
			pass

		else:
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

			try:
				with st.sidebar:
					# サイドバータイトル
					st.write('<span style="color:#006AB6; font-size: 14px; font-weight : bold;"> \
						データカタログ情報を表示するテーブルの検索条件を指定してください</span>''', \
						unsafe_allow_html=True)

					# データベース選択リストの表示
					if dispSideDatabaseList(cs) == False:
						st.error("データベースが存在しません（アカウントにデータベースが存在する場合はユーザーの権限を確認してください）。")
						pass

					# データベース選択ボックス作成
					st.session_state["データベース選択"] = st.selectbox(
						' データベース選択：',
						st.session_state["area_list1"]
						, key = 'データベース名'
					)

					# スキーマ選択リストの表示
					if dispSideSchemaList(cs) == False:
						st.error("スキーマが存在しません。")
						pass					

					# スキーマ選択ボックス作成
					st.selectbox(
						' スキーマ選択：',
						st.session_state["area_list3"]
						, key = 'スキーマ名'
					) 

					# デザイン補正(空行表示)
					st.write(" ")

					# 検索ボックス表示
					st.session_state["search_table"] = st.text_input('テーブル情報から検索', help='テーブル名とテーブルのコメント情報から検索します') 
					st.session_state["search_column"] = st.text_input('カラム情報から検索', help='カラム名とカラムのコメント情報から検索します')
					st.write(" ")

					# テーブル選択リスト(フォーム)の表示
					if  dispSideTableList(cs) == False:
						st.error("テーブル選択リストを表示できません。")
						pass						 

					# テーブル選択フォーム表示
					with st.form(key = "form"):
						st.selectbox(
							' テーブル選択：',
							st.session_state["my_list3"]
						, key = "テーブル名"
						) 
						
						# 処理カウント初期化
						if 'count' not in st.session_state: 
							st.session_state.count = 0 

						# 表示ボタン押下時にメイン画面描画開始
						increment = st.form_submit_button("表示", on_click=dispMainPage)

						# 処理が行われた場合、処理カウントをインクリメント
						if increment:
							st.session_state.count += 1

			# 検索結果を確認
			except snowflake.connector.errors.DatabaseError:
				st.title("データカタログ")
				st.info("選択した条件に合致するテーブルが存在しません。")
				pass

			finally:
				with st.sidebar:
					st.write(" ")
					st.write(" ")
					# アカウント名表示
					image = Image.open(snow_image)
					st.image(image, use_column_width=False)
					st.caption("アカウント名")
					st.caption(sf_account)
					st.caption("ユーザー名")
					st.caption(sf_user)

					# トップ画面に戻るボタンの作成
					st.button('''アカウントを切り替える''', on_click=returnPrevPage, help = "ユーザー名、ロール、アカウントを変更する")

##################################################
# ツール実行
##################################################
if ("page_control" in st.session_state and
st.session_state["page_control"] == 1):
	dispSidePage()
elif ("page_control" in st.session_state and
st.session_state["page_control"] == 2):
	disploginPageforBack()
else:
	st.session_state["page_control"] = 0
	disploginPage()
