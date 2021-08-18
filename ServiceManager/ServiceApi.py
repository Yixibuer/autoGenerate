# coding=utf-8
import time
import requests
import yaml
import json
import os
import sys


class ServiceApi:

    def __init__(self):
        self.json_path = self.getParentPath() + "/ServiceModel.json"
        self.yaml_path = self.getParentPath() + "/ServiceModel.yaml"
        self.username = self.yamlReader(self.yaml_path)['test_maolaozu']['username']
        self.password = self.yamlReader(self.yaml_path)['test_maolaozu']['password']

    def getParentPath(self):
        parent_dir = os.path.abspath(os.path.dirname(__file__))
        # print(parent_dir)
        return parent_dir

    def getJsonPath(self, json_name):
        json_path = self.getParentPath() + "/" + json_name + ".json"
        return json_path

    def readJsonFile(self, filepath):
        with open(filepath, 'r') as f:
            para = f.read()
        f.close()
        return para

    def rewriteJsonFile(self, filepath, json_data):
        with open(filepath, 'w') as f:
            json.dump(json_data, f)
        f.close()

    def getHeaders(self):
        headers = {
            'cookie': self.loadMaoServer(),
            'Content-Type': 'application/json',
            'authorization_type': '3'
        }
        return headers

    def yamlReader(self, yaml_path):
        f = open(self.yaml_path)
        d = f.read()
        yaml_reader = yaml.load(d, Loader=yaml.FullLoader)
        return yaml_reader

    def getRequestData(self, index, interface_name):
        with open(self.json_path, 'r+', encoding='UTF-8') as f2:
            para = f2.read()
            # print(type(para))
            para = json.loads(para)[index][interface_name]
            # print(para)
            data_search = json.dumps(para, indent=2)
            # print(data_search)
        return data_search

    def getTicket(self):
        """
        调用 url 获取验证码的方法
        使用白名单的pid直接获取到ticket
        :return: ticket给后面其他接口使用
        """
        # print(username)
        # ticket_url = "https://test-open-service.codemao.cn/captcha/rule"
        ticket_url = self.yamlReader(self.yaml_path)['url']['获取验证码接口']
        print(ticket_url)
        payload = "{\"identity\": \" %s \",\"pid\":\"hp_y9Wiw\",\"deviceId\":\"5d92ad9195ef099394ad786cc106d6f9\",\r\n    \"timestamp\": \" %s \"\r\n}" % (
            self.username, str(
                int(time.mktime(time.localtime()))))
        headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        response = requests.request("POST", url=ticket_url, headers=headers, data=payload)
        if response.status_code == 200:
            ticket = response.json()['ticket']
            # print(ticket)
            return ticket
        else:
            return False

    def loadMaoServer(self):
        """
        调用登录猫老祖后台的接口
        :return: test-admin-authorization所需要的token值
        test_internal_account_token所需要的token值
        """
        load_url = self.yamlReader(self.yaml_path)['url']['登录接口']
        load_parm = "{\n\"identity\": \"%s\",\r\n \"password\": \"%s\"\r\n}" % (self.username, self.password)
        headers = {
            'content-type': 'application/json;charset=UTF-8',
            'x-captcha-id': '',
            'x-captcha-ticket': '%s' % self.getTicket()
        }
        response = requests.request("POST", url=load_url, headers=headers, data=load_parm)
        # print(response)
        if response.status_code == 200:
            test_admin_authorization = "Bearer+" + response.json()['fishToken']
            # print(test_admin_authorization)
            test_internal_account_token = response.json()['token']
            # print(test_internal_account_token)
            return 'test-admin-authorization=%s;test_internal_account_token=%s;' % (
                test_admin_authorization, test_internal_account_token)
        else:
            print('连接猫老祖后台失败')
            return

    def createCourse(self):
        """
        调用新建课程的接口
        url = 'https://test-codecamp-admin.codemao.cn/admin/courses/base'
        :return: course_id
        """
        url = self.yamlReader(self.yaml_path)['url']['新建课程接口']
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        # print(data_search)
        response = requests.request("POST", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        print("创建成功,课程ID为:" + response.text)
        course_id = response.text
        return course_id

    def addCourseLink(self, course_id):
        """
        新建环节，包含特殊环节
        当前服务端报错500，"error_name":"kotlin.KotlinNullPointerException"
        :param course_id
        :return: link_id
        """
        url = self.yamlReader(self.yaml_path)['url']['新建环节接口'].replace("{course_id}", course_id)
        print(url)
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        response = requests.request("PUT", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        link_id = response.text
        print("link_id_list：%s" % link_id)
        return link_id

    def addInteractiveVideo2Link(self, course_id, link_id):
        """
        调用添加交互视频模式步骤接口
        :param course_id:
        :param link_id:
        :return:
        """
        url = self.yamlReader(self.yaml_path)['url']['添加交互视频步骤到环节接口'].replace("{course_id}", course_id).replace("{link_id}", link_id)
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        response = requests.request("PUT", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        print(response.text)
        return

    def addMultiStep2Link(self, course_id, link_id):
        """
        调用添加多步骤接口
        :param course_id:
        :param link_id:
        :return:
        """
        url = self.yamlReader(self.yaml_path)['url']['添加多步骤到环节接口'].replace("{course_id}", course_id).replace("{link_id}", link_id)
        print(url)
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        response = requests.request("PUT", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        print(response.status_code)
        return

    def createPackage(self):
        """
        调用新建课包接口
        :return:package_id
        """
        url = self.yamlReader(self.yaml_path)['url']['新建课包接口']
        print(url)
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        response = requests.request("POST", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        get_response = response.json()
        # print(type(get_response))
        if 'data' in get_response:
            if 'packageId' in get_response['data']:
                package_id = get_response['data']['packageId']
                print("创建成功,课程包ID为:%s" % package_id)
                return package_id
            else:
                return False
        else:
            return False

    def createChapters(self, package_id):
        """
        创建课包内章节，创建章节时，ID可以等于0
        :param package_id:
        :return:
        """
        url = self.yamlReader(self.yaml_path)['url']['新建章节接口'].replace("{package_id}", str(package_id))
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        response = requests.request("POST", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        print(type(response))
        get_response = response.json()
        print(type(get_response))
        if response.status_code == 200:
            print('创建章节成功：%s' % response.text)
            return response.text
        else:
            print('创建章节失败')
            return False

    def getChaptersId(self, package_id):
        url = self.yamlReader(self.yaml_path)['url']['获取章节ID接口'].replace("{package_id}", str(package_id))
        reponse = requests.request("GET", url=url, headers=self.getHeaders(), data="")
        print(reponse.text)
        data = reponse.json()["data"]
        chapter_id_list = []
        for i in data:
            chapter_id_list.append(i['id'])
            print(chapter_id_list)
        return chapter_id_list

    def addCourse2Chapter(self, chapter_id):
        """
        向章节内增加课程
        :param chapter_id:
        :return:
        """
        url = self.yamlReader(self.yaml_path)['url']['向章节内添加课程接口'].replace("{chapter_id}", str(chapter_id))
        print(url)
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        response = requests.request("POST", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        if response.status_code == 200:
            print('向章节内添加课程成功：%s' % response.status_code)
            return response.text
        else:
            print(response.text + '向章节内添加课程失败')
            return

    def addPackageSKU(self, package_id):
        """
        增加课程包商品信息配置，增加后可以上线课包
        :param package_id:
        :return:
        """
        url = self.yamlReader(self.yaml_path)['url']['增加课程包商品信息配置'].replace('{package_id}', str(package_id))
        print(url)
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        # print(type(data_search))
        response = requests.request("POST", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        get_response = response.json()
        # print(type(get_response))
        print(response.text)
        return

    def packageState1(self, package_id):
        """
        上线课程包，默认state：1，代表上线
        :param package_id:
        :return:
        """
        url = self.yamlReader(self.yaml_path)['url']['上线课程包'].replace('{package_id}', str(package_id))
        print(url)
        para = {'state': 1}
        response = requests.request("PUT", url=url, headers=self.getHeaders(), params=para)
        print(response.text)
        # print(response.url)
        if response.status_code == 200:
            print('上线课包成功')
            return
        else:
            print('上线课包失败')
            print(response.text)
            return False

    def createTerm(self):
        """
        调用新建课期的接口
        :return: term_id
        """
        url = self.yamlReader(self.yaml_path)['url']['新建课期']
        print(url)
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        # print(type(data_search))
        response = requests.request("POST", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        get_response = response.json()
        print(get_response)
        if 'data' in get_response:
            if 'termId' in get_response['data']:
                term_id = get_response['data']['termId']
                print("创建成功,课期ID为:" + str(term_id))
                return term_id
            else:
                print("创建失败")
                print(response.text)
                return False
        else:
            print('创建失败')
            print(response.text)
            return False

    def termUnlockTime(self, term_id):
        """
        设置课期解锁时间
        :return:
        """
        url = self.yamlReader(self.yaml_path)['url']['设置课期解锁时间'].replace('{term_id}', str(term_id))
        print(url)
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        response = requests.request("POST", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        get_response = response.json()
        # print(get_response)
        if response.status_code == 200:
            print('设置课期解锁时间成功')
            return
        else:
            print('设置课期解锁时间失败')
            print(response.text)
            return False

    def termSchedule(self, term_id):
        url = self.yamlReader(self.yaml_path)['url']['课期排课'].replace('{term_id}', str(term_id))
        print(url)
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        response = requests.request("PATCH", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        get_response = response.json()
        # print(get_response)
        if response.status_code == 200:
            print('排课成功')
            return
        else:
            print('排课失败')
            print(response.text)
            return False

    def createClass(self):
        """
        调用创建班级接口
        :return:
        """
        url = self.yamlReader(self.yaml_path)['url']['新建班级']
        print(url)
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        # print(data_search)
        response = requests.request("POST", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        get_response = response.json()
        # print(get_response)
        if response.status_code == 200:
            print('创建班级成功')
            return
        else:
            print('创建班级失败')
            print(response.text)
            return False

    def getClassId(self, term_id):
        """
        调用查询classID接口
        :param term_id:
        :return: class_id
        """
        url = self.yamlReader(self.yaml_path)['url']['获取班级ID']
        print(url)
        para = {'page': 1, 'limit': 10}
        response = requests.request("GET", url=url, headers=self.getHeaders(), params=para)
        # print(response.text)
        result = response.json()['data']['items']
        # print(result[0])
        for i in range(10):
            if result[i]["termId"] == int(term_id):
                print('class_id为: %s' % result[i]['classId'])
                class_id = result[i]['classId']
                return class_id
            else:
                print(response.text)
                continue

    def orderImport(self, phone_number, package_id, term_id, class_id):
        """
        :return:
        """
        url = self.yamlReader(self.yaml_path)['url']['订单导入接口']
        print(url)
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        encode_data = eval(data_search)
        encode_data_temp = encode_data[0]
        encode_data_temp["phone_number"] = phone_number
        encode_data_temp["package_id"] = package_id
        encode_data_temp["term_id"] = term_id
        encode_data_temp["class_id"] = class_id
        print(encode_data)
        self.rewriteJsonFile(self.getJsonPath((sys._getframe().f_code.co_name)), encode_data)
        data_search = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))

        response = requests.request("POST", url=url, headers=self.getHeaders(), data=data_search.encode('UTF-8'))
        if response.status_code == 200 and response.json()["success"] == 1:
            print('订单导入成功')
            return
        else:
            print('订单导入失败， %s' % response.text)
            return False

    def getQiniuToken(self):
        url = self.yamlReader(self.yaml_path)['url']['获取七牛token']
        response = requests.request("GET", url=url, headers=self.getHeaders(), data="")
        print(response.json()["token"])
        return response.json()["token"]

    def getQiniuLink(self, filename, content_type):
        url = self.yamlReader(self.yaml_path)['url']['获取七牛链接接口']
        data = self.readJsonFile(self.getJsonPath(sys._getframe().f_code.co_name))
        # data = data.replace("image/png", "mp3")
        # data = data.replace("dev/444/16188168813440.png", "dev/444/%s%s.%s" % (self.getMicroSecTimeStamp(), filename, content_type))
        headers = {
            "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundaryATRm9tFN2LjxXTBR",
            "token": self.getQiniuToken()
        }
        response = requests.request("POST", url=url, headers=headers, data=data)
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            qiniu_link = "https://dev-cdn-common.codemao.cn" + response.json()["key"]
            return qiniu_link
        else:
            return False


    def getMicroSecTimeStamp(self):
        t = time.time()
        time_stamp = int(round(t * 1000))  # 转换成毫秒时间戳
        return time_stamp

    def getSecTimeStamp(self, t):
        # t = time.time()
        print(time.time())
        time_stamp = (int(t))    # 转换成秒时间戳
        return time_stamp


class Basic:
    pass


if __name__ == '__main__':
    test = ServiceApi()
    test.loadMaoServer()
    # test.orderImport("15303002609", "1709", "2527", "8180")
    # test.createPackage()
    # test.addCourse2Chapter(1167)
    # test.addPackageSKU(3120)
    # test.packageState1(3120)
    test.createTerm()
    # test.orderImport(15641054931,1961,2864,8523)
    # test.createCourse
