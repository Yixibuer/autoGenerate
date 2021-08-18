# coding=utf-8
import ResourceManager.staticApi as staticApi
import ServiceManager.ServiceApi as serviceApi
import SceneManager.scene as scene


class Start:
    def start(self):
        if staticApi.ResVerifyManager().verifyAllRes():
            phone_number = input('请输入要导入课程的手机号：')
            while True:
                if len(phone_number) == 11:
                    '''
                    默认配置3个场景的课程
                    '''
                    print('正在创建课程-普通视频课')
                    course_id_list = []
                    course_id1 = scene.CourseScene().GeneralVideo(staticApi.ProvideManager().bcm_url,
                                                                  staticApi.ProvideManager().getPreviewUrl(),
                                                                  name="普通视频课")
                    course_id_list.append(course_id1)
                    print('正在创建课程-编程课非全局kids多步骤课程1')
                    course_id2 = scene.CourseScene().NotGlobalKidsAddMultiSteps("编程课非全局多步骤1")
                    course_id_list.append(course_id2)
                    print('正在创建课程-编程课非全局kids多步骤课程2')
                    course_id3 = scene.CourseScene().NotGlobalKidsAddMultiSteps("编程课非全局多步骤2")
                    course_id_list.append(course_id3)
                    print('正在创建课程-全局kids交互系统课1')
                    course_id4 = scene.CourseScene().GlobalKidsAddInteractiveVideo("编程非全局交互视频1")
                    course_id_list.append(course_id4)
                    print('正在创建课程-全局kids交互系统课2')
                    course_id5 = scene.CourseScene().GlobalKidsAddInteractiveVideo("编程非全局交互视频2")
                    course_id_list.append(course_id5)
                    course_name_list = ["普通视频课", "编程课非全局多步骤1", "编程课非全局多步骤2", "编程课非全局交互视频1", "编程课非全局交互视频2"]

                    print('正在创建编程课课包')
                    package_id = scene.PackageScene().ProgrammingPackage(course_id_list)
                    print('正在创建编程课期')
                    term_id = scene.TermScene().ProgrammingTerm(package_id, course_id_list, course_name_list)
                    print('正在创建班级')
                    class_id = scene.ClassScene().ProgrammingClass(package_id, term_id)
                    print('正在向手机号%s的账号中导入课程' % phone_number)
                    serviceApi.ServiceApi().orderImport(phone_number, package_id, term_id, class_id)
                    break
                else:
                    phone_number = input("请输入11位手机号码，请重新输入：")
                    continue


if __name__ == '__main__':
    while True:
        # line = input("请将配课所需要的配置素材按类别放置到不同的文件夹内，放置完成后点击回车，开始自动配课")
        line = input("请选择 1.已建好课程，新建课包/课期/班级/导入%n2.不会建课程，随便帮我建几节，导进手机号里就行")
        # print(line)
        if line == '1':
            test = Start()
            test.start()
            break
        if line == "2":
            pass
        else:
            continue



