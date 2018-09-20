from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


# Course -课程基本信息
# Lesson -章节信息
# Video  -视频
# CourseResource -课程资源


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u"课程名称")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(choices=(('cj', u'初级'), ('zj', u'中极'), ('gj', u'高级')), max_length=2, verbose_name="难度",
                              default='cj')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    student = models.IntegerField(default=0, verbose_name=u"学习人数")
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True, on_delete=models.CASCADE)
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面", max_length=100, blank=True)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    category = models.CharField(max_length=20, verbose_name="课程类别", default="后端开发")
    # 关键词
    tag = models.CharField(max_length=10, verbose_name="课程标签", default="")
    # 是否是放在轮播图中
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    # 课程须知
    you_need_know = models.CharField(max_length=200, verbose_name="课程须知", default="")
    teacher_tell = models.CharField(max_length=200, verbose_name="老师告诉你能知道什么", default="")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    # 调用外键所在模型的数据 统计章节数
    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()

    # 设置函数在后台的显示内容
    get_zj_nums.short_description = "章节数"

    # 设置一个跳转
    def go_to(self):
        from django.utils.safestring import mark_safe
        # 如果不调用mark safe 会将字符串进行转义保障安全
        return mark_safe("<a href='https://www.ruisfree.com'>跳转</a>")

    go_to.short_description = "跳转"

    # 获取学习该课程的用户有哪些
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    # 获取课程章节
    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


# 轮播课程model  集成Course
class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        # 设置之后不会生成一张表，只是为了在后台进行显示不同的数据
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程",
                               on_delete=models.CASCADE)  # django2.0以后需要加上 on_delete=models.CASCADE
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        # 获取章节视频
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"视频名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    url = models.CharField(max_length=200, verbose_name="访问地址", default="")
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name
