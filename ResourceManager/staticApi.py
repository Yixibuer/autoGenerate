import os
import time
import requests
import ServiceManager.ServiceApi as serviceApi


class ReceiveManager:
    def __init__(self):
        self.bcm_path = r"/Users/cm_1/PycharmProjects/AutoGenerate/static/bcm/bcm_url"
        self.cocos_js_path = r"/Users/cm_1/PycharmProjects/AutoGenerate/static/cocos_js"
        self.cocos_json_path = r"/Users/cm_1/PycharmProjects/AutoGenerate/static/cocos_json"
        self.cocos_zip_path = r"/Users/cm_1/PycharmProjects/AutoGenerate/static/cocos_zip"
        self.image_path = r"/Users/cm_1/PycharmProjects/AutoGenerate/static/image"
        self.itv_path = r"/Users/cm_1/PycharmProjects/AutoGenerate/static/itv"
        self.mp3_path = r"/Users/cm_1/PycharmProjects/AutoGenerate/static/mp3"
        self.mp4_path = r"/Users/cm_1/PycharmProjects/AutoGenerate/static/mp4"

    def getBcm(self):
        with open(self.bcm_path, 'r+', encoding='UTF-8') as bcm_file:
            bcm = bcm_file.read()
        print(bcm)
        return bcm

    def getImage(self):
        image_files = os.listdir(self.image_path)
        return image_files

    def getItv(self):
        itv_files = os.listdir(self.itv_path)
        return itv_files

    def getMp3(self):
        mp3_files = os.listdir(self.mp3_path)
        return mp3_files

    def getMp4(self):
        mp4_files = os.listdir(self.mp4_path)
        return mp4_files

    def getCocosJs(self):
        cocos_js_files = os.listdir(self.cocos_js_path)
        return cocos_js_files

    def getCocosJson(self):
        cocos_json_files = os.listdir(self.cocos_json_path)
        return cocos_json_files

    def getCocosZip(self):
        cocos_zip_files = os.listdir(self.cocos_zip_path)
        return cocos_zip_files


class ResVerifyManager:
    def __init__(self):
        pass

    def verifyBcm(self):
        """
        参考kids web检测小工具的方法检测bcm是否可以加载成功
        :return: 
        """""
        pass

    def verifyMp3(self):
        """

        :return:
        """

    def verifyMp4(self):
        pass

    def verifyImg(self):
        """
        检查image大小，缩略图需要小于100k
        :return:
        """

    def verifyAllRes(self):
        return True


class ProvideManager:
    def __init__(self):
        self.bcm_url = ReceiveManager().getBcm()
        self.service = serviceApi.ServiceApi()
        self.mp3 = ""
        self.itv = "https://dev-cdn-common.codemao.cn/dev/444/16176094775421612181345994c3.itv"
        self.png = "https://dev-cdn-common.codemao.cn/dev/444/16176098323151-奇梦岛生活记图标.png"

    def getPreviewUrl(self):
        preview_url = ReceiveManager().getImage()
        if len(preview_url) > 1:

            return preview_url[0]
        else:
            return preview_url














if __name__ == '__main__':
    test = ProvideManager()
    test.getPreviewUrl()