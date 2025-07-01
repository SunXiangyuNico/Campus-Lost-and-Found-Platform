from mongoengine import connect, disconnect
import os

# 定义一个函数来连接数据库
def connectDB():
    """
    从环境变量中读取 MONGO_URI 并连接到数据库。
    """
    try:
        # 使用 os.environ.get() 从环境变量中安全地获取连接字符串
        db_uri = os.environ.get('MONGO_URI')
        
        if not db_uri:
            raise Exception("MONGO_URI not found in environment variables")

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