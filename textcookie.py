from PyQt5.Qt import *
import requests,json,base64

class API(object):
    #下载验证码  GET
    GET_YZM_URL = "https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand"

    #校验验证码 POST
    # callback: jQuery191037043257607249735_1550240582305
    # answer: 188, 112, 128, 116
    # rand: sjrand
    # login_site: E
    # _: 1550240582307
    CHECK_YZM_URL = "https://kyfw.12306.cn/passport/captcha/captcha-check?callback"

class APITool(QObject):

    #保持会话，建立会话对象“客户端”，
    session = requests.session()

    @classmethod  #类方法，因为需要共用cookies，借此保持会话
    def download_yzm(cls):
        response = cls.session.get(API.GET_YZM_URL)
        _base64 = (response.json()["image"])
        content = base64.b64decode(_base64)
        #print(image)
        # print(response.content)
        # print(cls.session.cookies)
        with open("API/yzm.jpg","wb") as f:
            f.write(content)
        return "API/yzm.jpg"

    @classmethod
    def check_yzm(cls,yzm):
        data_dic = {
            #"callback": "jQuery191037043257607249735_1550240582305",
            "answer": yzm,
            "rand": "sjrand",
            "login_site": "E",
            #"_": "1550240582307"经过测试 "callback""_" 不加似乎不影响请求，具体后面才能知道！
        }
        response = cls.session.post(API.CHECK_YZM_URL,data=data_dic)
        #下面这几行个人认为处理不是很好，有自己改的，比较好的，可以下面回复
        for i in response.text:
            try:
                a = int(i)
                return a == 4
            except:
                pass
        #print(response.text)
        #print(response.json(["result_code"]))