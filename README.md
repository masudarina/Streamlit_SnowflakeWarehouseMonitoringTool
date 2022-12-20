
# Snowflake ウェアハウス監視ツール

## 概要

Snowflake ウェアハウス監視ツールは、Snowflakeのウェアハウスの状況を可視化するためのツールです。

## 前提条件
・Streamlit Cloud が使用できること 　アカウント作成ページ：https://share.streamlit.io/signup

## 設定手順
・Streamlit Cloud アプリデプロイ設定手順

	1. Streamlit Cloud アプリ作成画面の「New app」をクリックする

	2. 「Paste GitHub URL」をクリックする

	3. 下記のURLを貼る
	URL：
	https://github.com/masudarina/Streamlit_SnowflakeWarehouseMonitoringTool/blob/main/checkSnowflakeMain.py

・Streamlit Cloud アプリ共有設定手順

	1. Streamlit Cloud アプリ作成画面を開き、共有したいアプリの３点リーダーをクリックする

	2. 「Settings」＞「Sharing」をクリックする

	2. 「Invite viewers by email」に閲覧者のメールアドレスを記入し、「Save」をクリックする
	参考サイト：
	https://docs.streamlit.io/streamlit-cloud/get-started/share-your-app

## 使用手順

1. Streamitからの招待メールを開き、「Accept invite and visit app」を押下する

参考サイト： https://docs.streamlit.io/streamlit-cloud/get-started/share-your-app

2. Webブラウザ画面表示後、Snowflakeの認証情報を入力して「OK」ボタンを押下する

※Snowflake認証情報は以下を参考に入力する

アカウント名(必須) : Snowflakeのアカウント名 ユーザー名(必須) ： Snowflakeアカウント接続時のユーザー名 パスワード(必須) : ユーザーのパスワード ロール : ユーザーにデフォルトのロールが設定されていない場合は、使用するロールを記入 ウェアハウス : ユーザーにデフォルトのロールが設定されていない場合は、使用するロールを記入

※ツール確認用URL： https://masudarina-st-snowflake-checkwarehousestool-v20220729-01-qam7kk.streamlitapp.com/

新規作成　2022/07/28
