import json
from mongoengine import connect, disconnect
import os

# 定义一个函数来连接数据库
def connectDB():
    """
    读取配置文件并连接到 MongoDB 数据库。
    """
    try:
        # 读取同目录下的 default.json 文件来获取配置
        # __file__ 是当前脚本的路径，os.path.dirname(__file__) 获取当前目录
        config_path = os.path.join(os.path.dirname(__file__), 'default.json')
        
        with open(config_path) as config_file:
            config = json.load(config_file)
        
        # 从配置中获取 MongoDB 的连接字符串
        db_uri = config.get('mongoURI')
        
        if not db_uri:
            raise Exception("mongoURI not found in config file")

        # 使用 MongoEngine 连接到数据库
        connect(host=db_uri)
        
        print("MongoDB (Python) Connected...")

    except Exception as e:
        # 如果连接过程中发生任何错误，在控制台输出错误信息
        print(f"Error connecting to MongoDB: {e}")
        # 退出程序
        exit(1)

def disconnectDB():
    """
    断开与数据库的连接。
    """
    disconnect() 