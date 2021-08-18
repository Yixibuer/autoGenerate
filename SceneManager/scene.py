# coding=utf-8
import ServiceManager.ServiceApi as serviceApi
import ResourceManager.staticApi as staticApi
import json
import datetime


class CourseScene:
    def __init__(self):
        self.service = serviceApi.ServiceApi()
        # self.name = ""
        # self.yaml_path = r'/Users/cm_1/PycharmProjects/AutoGenerate/SceneManager/sceneModel.yaml'

    def GeneralVideo(self, bcm_url, preview_url, name, content_type=1, lesson_type=1, description=""):
        """
        测试编程普通视频课,bcm_url,course_name
        :return:
        """
        self.service.loadMaoServer()
        json_data = self.service.readJsonFile(self.service.getJsonPath("createCourse"))
        json_para = eval(json_data)
        json_para["preview_url"] = preview_url
        json_para["name"] = name
        json_para["lesson_type"] = lesson_type
        json_para["bcm_url"] = bcm_url
        self.service.rewriteJsonFile(self.service.getJsonPath("createCourse"), json_para)
        course_id = self.service.createCourse()
        return course_id

    def NotGlobalKidsAddMultiSteps(self, name, content_type=1, lesson_type=2, description=""):
        """
        content_type =1  为编程课
        lesson_type = 2 为交互系统课
        测试编程非全局+多步骤（多个环节同一个kids）
        :return:
        """
        # data = self.service.yamlReader(self.yaml_path)["非全局多步骤多环节相同bcm"]
        self.service.loadMaoServer()
        self.configNotGlobalKidsAddMultiSteps(name, lesson_type)
        course_id = self.service.createCourse()
        link_id_list = self.service.addCourseLink(course_id)
        link_id = link_id_list[1:5]
        result = self.service.addMultiStep2Link(course_id, link_id)
        print(result)
        return course_id

    def configNotGlobalKidsAddMultiSteps(self, name, lesson_type):
        json_data = self.service.readJsonFile(self.service.getJsonPath("createCourse"))
        json_para = eval(json_data)
        json_para["name"] = name
        json_para["lesson_type"] = lesson_type
        self.service.rewriteJsonFile(self.service.getJsonPath("createCourse"), json_para)

    def GlobalKidsAddInteractiveVideo(self, name, content_type=1, lesson_type=2, description=""):
        """
        测试编程全局kids+交互视频
        :return:
        """
        self.service.loadMaoServer()
        self.configGlobalKidsAddInteractiveVideo(name, lesson_type)
        course_id = self.service.createCourse()
        link_id = self.service.addCourseLink(course_id)[1:5]
        self.service.addInteractiveVideo2Link(course_id, link_id)
        return course_id

    def configGlobalKidsAddInteractiveVideo(self, name, lesson_type):
        json_data = self.service.readJsonFile(self.service.getJsonPath("createCourse"))
        json_para = eval(json_data)
        json_para["name"] = name
        json_para["lesson_type"] = lesson_type
        self.service.rewriteJsonFile(self.service.getJsonPath("createCourse"), json_para)
        print(json_para)


    def GlobalKidsAddMultiSteps(self,content_type=1, lesson_type=2, description=""):
        """
        测试编程全局kids+多步骤
        :return:
        """

        pass

    def AllKindsOfLinks(self,content_type=1, lesson_type=2, description=""):
        """
        包含各种类型的环节，课前预习、开始上课（交互视频+kids）、课后复习、H5环节、视频打卡、学习报告
        :return: status
        """
        pass


class PackageScene:
    def __init__(self):
        self.service = serviceApi.ServiceApi()

    def ProgrammingPackage(self, course_id_list, package_name="", platform=9, content_type=1, business_type=1, attribute=2):
        """
        课包设置：小火箭/kids/编程课/正式课
        课期设置：招生开始时间/结束时间/开营时间/结营时间
        课包内容：
            第一章设置：章节名称5个字
            第二章：章节名称20个字
        :return:
        """
        self.service.loadMaoServer()
        package_id = self.service.createPackage()
        self.service.createChapters(package_id)
        chapter_id_list = self.service.getChaptersId(package_id)
        # # 根据章节个数向每个章节内添加
        i = 0
        while i < len(chapter_id_list):
            self.configAddCourse2Chapter(course_id_list, i)
            self.service.addCourse2Chapter(chapter_id_list[i])
            i = i + 1
        self.service.addPackageSKU(package_id)
        self.service.packageState1(package_id)
        return package_id

    def configAddCourse2Chapter(self, course_id_list, i):
        """
        固定配置： 新建课包/新建章节
        需要重写配置：向章节内添加课程
        i 是在第1次调用修改配置时，添加course_id_list里面的前面一半课程到第1个章节里，后面一半的课程添加到第2个章节里
        :return:
        """
        if i == 0:
            self.service.rewriteJsonFile(self.service.getJsonPath("addCourse2Chapter"), course_id_list[:i+2])
            print("course_id_list:%s" % course_id_list[:i+2])
            return
        if i == 1:
            self.service.rewriteJsonFile(self.service.getJsonPath("addCourse2Chapter"), course_id_list[i+1:])
            print('course_id_list:%s' % course_id_list[i+1:])
            return
        else:
            print("error")
            return


class TermScene:
    def __init__(self):
        self.service = serviceApi.ServiceApi()

    def ProgrammingTerm(self, package_id, course_id_list, course_name_list, index="测试第一期"):
        """
        课期设置：编程课/小火箭/正式课
        课期名称：测试课期1
        :return:
        """
        self.service.loadMaoServer()
        self.configCreateTerm(package_id)     # 先配置新建课期的内容，再新建课期
        term_id = self.service.createTerm()
        self.service.termUnlockTime(term_id)
        self.configTermSchedule(course_id_list, course_name_list)
        self.service.termSchedule(term_id)
        return term_id

    def configCreateTerm(self, package_id):
        """
        省略了配置商品的步骤，使用固定的sku
        :param startTime: 早于当前时间10天
        :param endTime: 早于当前时间1天
        :param termBeginTime: 当前时间
        :param termFinishTime: 晚于当前时间10天
        """
        data = self.service.readJsonFile(self.service.getJsonPath("createTerm"))
        current_date = datetime.datetime.now()  # 获取当前时间 年月日时分秒
        startTime_temp = current_date + datetime.timedelta(days=-10)
        startTime = str(startTime_temp.timestamp()).split(".")[0]
        endTime_temp = current_date + datetime.timedelta(days=-1)
        endTime = str(endTime_temp.timestamp()).split(".")[0]
        termBeginTime_temp = current_date + datetime.timedelta()
        termBeginTime = str(termBeginTime_temp.timestamp()).split(".")[0]
        termFinishTime_temp = current_date + datetime.timedelta(days=+10)
        termFinishTime = str(termFinishTime_temp.timestamp()).split(".")[0]
        json_para = eval(data)
        json_para["packageId"] = package_id
        json_para["startTime"] = startTime
        json_para["endTime"] = endTime
        json_para["termBeginTime"] = termBeginTime
        json_para["termFinishTime"] = termFinishTime
        self.service.rewriteJsonFile(self.service.getJsonPath("createTerm"), json_para)
        print(self.service.readJsonFile(self.service.getJsonPath("createTerm")))

    def configTermSchedule(self, course_id_list, course_name_list):
        data = self.service.readJsonFile(self.service.getJsonPath("termSchedule"))
        encode_data = eval(data)
        json_para = encode_data["attendPlans"]
        # print(json_para)
        current_date = datetime.datetime.now()  # 获取当前时间 年月日时分秒
        unlock_time_temp = current_date + datetime.timedelta()   # unlocktime 默认设置所有的课程当前时间解锁
        unlock_time = str(unlock_time_temp.timestamp()).split(".")[0]
        length = len(json_para)
        for index in range(length):
            if index < len(course_id_list):
                data = json_para[index]
                data["index"] = index
                data["courseId"] = course_id_list[index]
                data["courseName"] = course_name_list[index]
                data["unlockTime"] = unlock_time
        self.service.rewriteJsonFile(self.service.getJsonPath("termSchedule"), encode_data)


class ClassScene:
    def __init__(self):
        self.service = serviceApi.ServiceApi()

    def ProgrammingClass(self, package_id, term_id):
        """
        班级设置：
        班级名称：测试班级1
        :return:
        """
        service = serviceApi.ServiceApi()
        self.configCreateClass(package_id, term_id)
        service.createClass()
        class_id = service.getClassId(term_id)
        return class_id

    def configCreateClass(self, package_id, term_id):
        data = self.service.readJsonFile(self.service.getJsonPath("createClass"))
        encode_data = eval(data)
        print(encode_data)
        encode_data["packageId"] = package_id
        encode_data["termId"] = term_id
        self.service.rewriteJsonFile(self.service.getJsonPath("createClass"), encode_data)


if __name__ == '__main__':
    test = ClassScene()
    # test.ProgrammingClass("1706", "2525")
    # test = TermScene()
    # test.configCreateTerm(3120)
    # test.
