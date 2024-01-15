from flask import Flask ,render_template ,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
import json
from datetime import datetime

app=Flask(__name__) #__name__ 代表目前執行的模組

# 配置數據庫連接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:fkfk0955011332@LAPTOP-80DSRMSI/yunzoexinkon?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 创建SQLAlchemy实例
db = SQLAlchemy(app)

class personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Airpressure = db.Column(db.Float, unique=False, nullable=False)
    Temperatue = db.Column(db.Float, unique=False, nullable=False)
    Orpvalue = db.Column(db.Float, unique=False, nullable=False)
    Nowtime = db.Column(db.DateTime,default=datetime.now)
    
    

# 在這裡手動進入應用程序上下文
with app.app_context():
    # 創建數據庫表
    db.create_all()

@app.route("/") #函式的裝飾 (Decorator): 以函式為基礎，提供附加的功能
def home():
    
    return "Hello Flask 2"

@app.route("/value",methods=["post"]) # @代表我們要處理的網站路徑
def test():
    print(json.dumps(request,default=str))
    #print(request.get_json())
    print(request.json)
    #print(dir(request))
    pressure = request.json["Pressure"]
    temperatue = request.json["Temperature"]
    orpvalue = request.json["ORP"]
    #print(pressure,temperatue,orpvalue)
    db.session.add(personal(Airpressure = pressure ,Temperatue = temperatue,Orpvalue = orpvalue))
    db.session.commit()
    return "success"

if __name__=="__main__" : #如果以主程式執行
    app.run(debug=True,host="0.0.0.0",port=500) #立刻啟動伺服器