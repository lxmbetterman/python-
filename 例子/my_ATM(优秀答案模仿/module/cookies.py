# -*- coding: utf-8 -*-
# __author__ = "LXM"
# Date: 2018/4/19 0019
import os, json, time
from .handle_hash import Handlehash

'''
cookie 数据结构  主要是利用 sessionid字段
    {
    "cookie": "5faa7929070a00ea62cb2e845bd5b4fd2c04bbc5",  #貌似无用 删除吧
    "sessionid": "6ac7d6337143a3932d9de190044ecd2691d3b4f4", 
    "times": 3600, 
    "status": true,
    "createtime": 1524138589.4231675
     }
     
     设置cookie时我们总是给"sessionid"字段赋值
'''
'''
    一个cookie对象应该包含的基本函数
    1、判断放cookie文件的文件夹是否存在
    2、生成cookie文件夹
    3、获取cookie 文件夹 和 文件 路径
    4、判断Cookie是否有效
    
    ...
    
    
'''


class Cookie:
    def __init__(self):
        self.__systemType = os.name
        self.__create_dir()  # 使用cookie必须调用

    ''' 判断需要的 文件夹 是否存在 '''

    def __dir_is_exist(self, path):
        if os.path.isdir(path):
            return True
        else:
            return False

    '''根据__systemType创建文件夹 return:False/True'''

    def __create_dir(self):
        if self.__systemType == "nt":
            paths = "C:\\.cookie"
            if not self.__dir_is_exist(paths):
                try:
                    os.makedirs(paths)
                    return True
                except Exception as e:
                    print(e)
                    return False
            return True
        elif self.__systemType == "posix":
            paths = "/User/cookiess"
            if not self.__dir_is_exist(paths):
                try:
                    os.makedirs(paths)
                    return True
                except Exception as e:
                    # Loggs().Error(str(e) + "CookiePath创建失败！")
                    print(e)
                    return False
        else:
            return False

    ''' 获取当前系统Cookie 文件夹 路径 '''

    def __getCookieDirPath(self):
        Wpaths = "C:\\.cookie"
        Mpaths = "/User/cookiess"
        if self.__systemType == "nt" and self.__dir_is_exist(Wpaths):
            return Wpaths
        elif self.__systemType == "posix" and not self.__dir_is_exist(Mpaths):
            return Mpaths
        else:
            return False

    ''' 获取当前系统Cookie 文件 路径 '''

    def __getCookiefilePath(self):
        paths = self.__getCookieDirPath()
        cookie_paths = os.path.join(paths, "cookie.json")
        if os.path.isfile(cookie_paths):
            return cookie_paths
        else:
            return False

    # def __MakeCookie(self, key):
    #     return Handlehash().encode_hash("cookie_" + key)

    ''' 判断Cookie是否有效(过期时间是否超过'''

    def __cookieIsUtilize(self):
        cookie_path = self.__getCookiefilePath()
        reads = ""
        count = False
        with open(cookie_path, "r") as f:
            reads = json.loads(f.read())
            times = reads["times"] #保质期
            Ttime = reads["createtime"] # 创建时间
            if int(time.time()) - times > Ttime: #失效
                count = True
            else:
                count = False
        if count:
            with open(cookie_path, "w") as f:
                reads["status"] = False
                json.dump(reads, f)
                return False
        else:
            return True

    '''获取cookie'''

    def __getitem__(self, item):  # item =="sessionid"
        """
        :param item: "sessionid" 字符串
        :return:  sessionid的值，这个值是在登录的时候生成的 参看Session.py中__createSession
        应该是把当前时间的时间戳加密，然后在用这个值在DB_session中去找session
        """
        count = False

        cookie_path = self.__getCookiefilePath()
        if cookie_path:
            with open(cookie_path, "r") as f:
                #  继续探索
                result = json.load(f)
                if result["status"]:
                    if self.__cookieIsUtilize():
                        return result["sessionid"]
                    else:
                        return False
                else:
                    return False

        else:
            return False

    '''设置cookie值'''

    def __setitem__(self, key, value):
        """
        :param key: "sessionid"
        :param value: " sessionid 对应的值"
        """
        cookieFilePath = self.__getCookiefilePath()  #文件不存在返回False
        if not cookieFilePath:
            cookieFilePath=os.path.join(self.__getCookieDirPath(), "cookie.json")
        # cookieId = self.__MakeCookie(key)
        if cookieFilePath:
            cookie = {key: value, "times": 3600, "status": True, "createtime": time.time()}
            with open(cookieFilePath,"w") as f:
                json.dump(cookie,f)
                return True
        else:
            return False
