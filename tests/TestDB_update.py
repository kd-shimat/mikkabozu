#!/usr/bin/env python
# ユニットテスト用ライブラリ
import unittest
import os

# SQLAlchemyを使う、テーブルの構成は自動モードにする
from sqlalchemy.ext.automap import automap_base

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# 環境変数 MYSQL_USER の値を DBUSER 変数に代入
DBUSER = os.getenv('MYSQL_USER')
# 同様にMYSQL_PASSWORDとMYSQL_DATABASEを取得
DBPASS = os.getenv('MYSQL_PASSWORD')
DBHOST = "db"
DBNAME = os.getenv('MYSQL_DATABASE')
# 接続文字列を作成し、dburlとする
dburl = f"mysql+mysqlconnector://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"

# DB接続用のエンジンを作成
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# リモートサーバーのアドレス
REMOTE_URL = 'http://selenium:4444/wd/hub'


# ユニットテスト用のクラスを作成
class TestDBAlchemy(unittest.TestCase):
    # テストケース実行前に呼ばれるメソッド
    def setUp(self):
        import mysql.connector
        # DBに接続
        self.engine = create_engine(dburl)
        # mysql-connector-pythonを使ってdb/person.sqlファイルを読み込んでテーブルを再初期化する
        with mysql.connector.connect(user=DBUSER, password=DBPASS, host=DBHOST, database=DBNAME) as conn:
            cursor = conn.cursor()
            with open("db/person.sql") as f:
                data = f.read()
                for sql in data.split(";"):
                    sql.strip()
                    sql = sql.replace("\n","")
                    cursor.execute(sql)
        self.driver = webdriver.Remote(REMOTE_URL, options=webdriver.ChromeOptions())

        # automap_base()を使ってテーブル構成を自動取得
        self.Base = automap_base()
        self.Base.prepare(autoload_with=self.engine)
        # セッションを取得
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self) -> None:
        self.session.close()
        self.driver.quit()

    def test_call_dbupdate_and_modified_goro(self):
        self.driver.get("http://web/dbupdate.php")
        self.driver.get_screenshot_as_file("results/01-dbupdate.png")
        self.Person = self.Base.classes.person
        data = self.session.query(self.Person).filter(self.Person.name.like('%野口五郎')).all()
        self.assertTrue(len(data) >= 1)

if __name__ == '__main__':
    unittest.main()
