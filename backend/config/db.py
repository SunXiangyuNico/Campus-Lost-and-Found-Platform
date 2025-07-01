from mongoengine import connect
import os
import certifi

def initialize_db(app):
    """
    初始化数据库连接。
    从 Flask app.config 中获取 URI。
    """
    mongo_uri = app.config.get('MONGO_URI')

    if not mongo_uri:
        raise ValueError("MONGO_URI not found in Flask app.config!")

    try:
        ca = certifi.where()
        connect(
            host=mongo_uri, 
            alias='default', 
            serverSelectionTimeoutMS=30000,
            tlsCAFile=ca
        )
        print("MongoDB (Python) Connected...")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")