# coding: utf-8
# python 3
from datetime import datetime 
from abc import ABC ,abstractmethod #抽象方法装饰器
import time
import random
import sys
# 抽象观察者接口
class Observer(ABC):
    @abstractmethod
    def update(self, SendName, message, timestamp):
        pass    #不实现内容
# 抽象被观察者接口
class Observable(ABC):
    @abstractmethod
    def add_user(self, observer):
        pass

    @abstractmethod
    def move_user(self, observer):
        pass

    @abstractmethod
    def notify(self, message):#通知抽象方法
        pass
# 用户类，实现 Observer 接口
class User(Observer):
    def __init__(self, name):
        self.name = name
        
    # 当被观察者调用 notify_observers 时，会触发update
    #                公众号名字  信息    时间戳
    def update(self, SendName, message, timestamp):
        print(f"{self.name} 收到来自【{SendName}】的消息：{message}（时间：{timestamp}）")
        self.auto_reply(SendName, message, timestamp)

    def auto_reply(self, SendName, message, timestamp):
        #模拟用户输入
        print(f"{self.name} 正在输入中", end="")
        for _ in range(3):
            time.sleep(0.5)
            print(".", end="")
            sys.stdout.flush()
        print()  # 换行
        time.sleep(random.uniform(0.5, 3)) #假装延迟，模拟思考
        now_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{self.name} 已回复：【{SendName}】我已阅读：“{message}” 时间：{now_time}")

# 公众号类，实现 Observable 接口
class public_account(Observable):
    def __init__(self, name):
        self.name = name    #          key->value     
        self.all_user = {} #hashmap name->observer

    def add_user(self, observer):
        if observer.name not in self.all_user:
            self.all_user[observer.name]=observer

    def move_user(self, observer):
        if observer.name in self.all_user:
            del self.all_user[observer.name]

    def notify(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n[公众号] 【{self.name}】发送消息：{message}（时间：{timestamp}）")
        for observer in self.all_user.values():
            observer.update(self.name, message, timestamp)

    def input_and_send(self):
        while True:
            msg = input(f"\n【{self.name}】请输入要发布的内容（输入 exit 退出）：\n> ")
            if msg.lower() == "exit":
                print("退出公众号消息输入。")
                break
            self.notify(msg)


if __name__ == "__main__":
    account = public_account("每日新闻")
    alice = User("Alice")
    bob = User("Bob")
    account.add_user(alice)
    account.add_user(bob)

    account.input_and_send()
