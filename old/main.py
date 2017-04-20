from login import fuck_bilibili
import os
import time

if '__main__' == __name__:
    isLogin = 0
    isReSet = 0
    fuck = fuck_bilibili()
    fuck.init()
    print("初始化帐户成功!")
    while True:
        fuck.showIndex()
        try:
            id = int(input("请输入: "))
            os.system("cls")
            if 1 == id:
                print("将会登陆 %s" % fuck.userid)
                fuck.Login(isReSet)
                isLogin = 1
            elif 2 == id:
                fuck.writeConfig(1)
                os.system("cls")
                print("重设帐户成功!")
                isReSet = 1
            elif 3 == id:
                print("再见 : )")
                fuck.p.terminate()
                fuck.p.join()
                time.sleep(1)
                os.system("cls")
                exit(0)

            if isLogin:
                if 4 == id:
                    try:
                        fuck.tm_hour, fuck.tm_min, fuck.tm_sec = input("请输入时间(时,分,秒, 以','隔开, 默认0,15,0): ").split(',')
                        if '' == fuck.tm_hour:
                            fuck.tm_hour = 0
                        if '' == fuck.tm_min:
                            fuck.tm_min = 15
                        if '' == fuck.tm_sec:
                            fuck.tm_sec = 0
                        print("签到时间为每天的%s:%s:%s" % (fuck.tm_hour, fuck.tm_min, fuck.tm_sec))
                        fuck.p.start()
                    except ValueError as e:
                        print("输入错误!")

        except ValueError as e:
            print("%s\n请输入数字!" % e)
