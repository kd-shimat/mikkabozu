import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.automap import automap_base
from selenium import webdriver
import os

# リモートサーバーのアドレス
REMOTE_URL = 'http://selenium:4444/wd/hub'

# 環境変数 MYSQL_USER の値を DBUSER 変数に代入
DBUSER = os.getenv('MYSQL_USER')
# 同様にMYSQL_PASSWORDとMYSQL_DATABASEを取得
DBPASS = os.getenv('MYSQL_PASSWORD')
DBHOST = "db"
DBNAME = os.getenv('MYSQL_DATABASE')
# 接続文字列を作成し、dburlとする
dburl = f"mysql+mysqlconnector://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"

def setup_test_db():
    # DBに接続
    engine = create_engine(dburl)

    # mysql-connector-pythonを使ってdb/person.sqlファイルを読み込んでテーブルを再初期化する
    with mysql.connector.connect(user=DBUSER, password=DBPASS, host=DBHOST, database=DBNAME) as conn:
        cursor = conn.cursor()
        with open("db/person.sql") as f:
            data = f.read()
            for sql in data.split(";"):
                sql.strip()
                sql = sql.replace("\n","")
                cursor.execute(sql)

    # Selenium Gridに接続しておく
    driver = webdriver.Remote(REMOTE_URL, options=webdriver.ChromeOptions())

    # automap_base()を使ってテーブル構成を自動取得
    Base = automap_base()
    Base.prepare(autoload_with=engine)
    # セッションを取得
    Session = sessionmaker(bind=engine)
    session = Session()

    return engine, driver, Base, session

def teardown_test_db(session, driver):
    session.close()    # DB接続セッションを閉じる
    driver.quit()      # Seleniumも閉じる
