#!/usr/bin/env python
# ユニットテスト用ライブラリ
# SQLAlchemyを使う、テーブルの構成は自動モードにする

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from test_setup import setup_test_db, teardown_test_db
import unittest
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker



# 環境変数 MYSQL_USER の値を DBUSER 変数に代入
DBUSER = os.getenv('MYSQL_USER')
# 同様にMYSQL_PASSWORDとMYSQL_DATABASEを取得
DBPASS = os.getenv('MYSQL_PASSWORD')
DBHOST = "db"
DBNAME = os.getenv('MYSQL_DATABASE')
# 接続文字列を作成し、dburlとする
dburl = f"mysql+mysqlconnector://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"



# ユニットテスト用のクラスを作成
class TestDBAlchemy(unittest.TestCase):
    # テストケース実行前に呼ばれるメソッド
    def setUp(self):
        self.engine, self.driver, self.Base, self.session = setup_test_db()

    def tearDown(self) -> None:
        teardown_test_db(self.session, self.driver)

    def test_call_dbdelete_and_check_fukazawa(self):
        """dbinsert.phpにアクセスした後、DBのpersonテーブルを確認し、'深沢七郎'がnameに含まれるレコードがないことを確認する"""

        # テスト用に「深沢七郎」のデータを投入する
        self.Person = self.Base.classes.person
        new_person = self.Person(name='深沢七郎', company_id = 2, age = 29)
        self.session.add(new_person)
        self.session.commit()

        # dbdelete.phpにアクセス(→正しく動けば深沢七郎のレコードが消えるはず)
        self.driver.get("http://web/dbdelete.php")
        self.driver.get_screenshot_as_file("results/03-dbdelete.png")

        # dbdeleteによりテーブル状態が書き換えられているはずなのでそれに同期して…
        self.session.commit()

        # 現状でクエリを出して0件になったことを確認する
        data = self.session.query(self.Person).filter(self.Person.name.like('%深沢七郎%')).all()
        self.assertTrue(len(data) < 1)

if __name__ == '__main__':
    unittest.main()
