from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error


app = Flask(__name__)
api = Api(app)
df = pd.read_csv(r'C:\Users\jujuc\NoteBook\Python\CoinMarketCap.csv', sep=",", header=1)
config = {
    'user': 'root',
    'password': 'password',
    'host': '127.0.0.1',
    'database': 'crypto_projet',
    'raise_on_warnings': True
}
post_args = reqparse.RequestParser()
post_args.add_argument("ID", type=int, required=False)
post_args.add_argument("Date", type=str, required=True)
post_args.add_argument("Open", type=float, required=True)
post_args.add_argument("High", type=float, required=True)
post_args.add_argument("Low", type=float, required=True)
post_args.add_argument("Close", type=float, required=True)
post_args.add_argument("Volume", type=float, required=True)
post_args.add_argument("MarketCap", type=float, required=True)
post_args.add_argument("Crypto", type=str, required=True)


def insert_database(config, query):

    conn = msql.connect(**config)

    if conn.is_connected():
        cursor = conn.cursor()
        sql=query
        cursor.execute(sql)
        cursor.close()
        conn.close()


def get_database(config, query):
    conn = msql.connect(**config)

    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return data


try:
    sql = "DROP TABLE IF EXISTS `space_crypto`; CREATE TABLE space_crypto(" \
              "ID int auto_increment," \
              "Date varchar(20)," \
              "Open float," \
              "High float," \
              "Low float," \
              "Close float," \
              "Volume float," \
              "MarketCap float," \
              "Crypto varchar(10)," \
              "PRIMARY KEY(ID));INSERT INTO crypto_projet.space_crypto VALUES (%s,%s,%s,%s,%s,%s,%s);"
    insert_database(config, sql)

    conn = msql.connect(**config)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        for i, row in df.iterrows():
            sql = "INSERT INTO crypto_projet.space_crypto VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
        cursor.close()

except Error as e:
    print("Error while connecting to MySQL", e)


class MyDatabase(Resource):
    def get(self):
        data = get_database(config, "select * from crypto_projet.space_crypto")
        return {'data': data}, 200  # return data and 200 OK


class MyAPI(Resource):
    def get(self, _id):
        data = get_database(config, "select * from crypto_projet.space_crypto where ID = {}".format(_id))
        return {'data': data}, 200  # return data and 200 OK

    def delete(self, _id):
        data_deleted = get_database(config, "select * from crypto_projet.space_crypto where ID = {}".format(_id))
        get_database(config, "delete from crypto_projet.space_crypto where ID = {}".format(_id))
        return {"deleted" : data_deleted}

    def post(self, _id):
        list_val = post_args.parse_args()
        get_database(config, "insert into crypto_projet.space_crypto(Date, Open, High, Low, Close, Volume, MarketCap, Crypto) values('{}', {}, {}, {}, {}, {}, {}, '{}')".format(list_val['Date'], list_val['Open'], list_val['High'], list_val['Low'], list_val['Close'], list_val['Volume'], list_val['MarketCap'], list_val['Crypto']))
        return {"data": request.json}

    def put(self, _id):
        list_val = post_args.parse_args()
        print("ici :", list_val)
        if get_database(config, "select * from space_crypto where ID = {}".format(_id)):
            get_database(config, "update crypto_projet.space_crypto set Date = '{}', Open = {}, High = {}, Low = {}, Close = {}, Volume = {}, MarketCap = {}, Crypto = '{}' where ID = {}".format(list_val['Date'], list_val['Open'], list_val['High'], list_val['Low'], list_val['Close'], list_val['Volume'],  list_val['MarketCap'], list_val['Crypto'], _id))
        else:
            get_database(config, "insert into crypto_projet.space_crypto(ID, Date, Open, High, Low, Close, Volume, MarketCap, Crypto) values({}, '{}', {}, {}, {}, {}, {}, {}, '{}')".format(_id, list_val['Date'], list_val['Open'], list_val['High'], list_val['Low'], list_val['Close'], list_val['Volume'], list_val['MarketCap'], list_val['Crypto']))
        return {"data": request.json}


api.add_resource(MyDatabase, '/mydatabase')
api.add_resource(MyAPI, '/myapi/<_id>')

if __name__ == '__main__':
    app.run()  # run our Flask app


