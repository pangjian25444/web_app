import datetime
from django.db import models
import time

# Create your models here.
from django.utils import timezone


class Subject(models.Model):
    name = models.CharField(max_length=20, verbose_name="科目")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "学科表"


class Course(models.Model):
    name = models.CharField(max_length=20, verbose_name="课程")

    subject = models.ManyToManyField(Subject, through="CourseANDSubject", verbose_name="包含学科")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = "课程类型表"


class ClassName(models.Model):
    name = models.CharField(max_length=20, verbose_name="班级")

    join_time = models.DateField(default=timezone.now, verbose_name="开学时间")

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="所属类型")

    def __str__(self):
        return f"{self.name},{self.course}"

    class Meta:
        verbose_name_plural = verbose_name = "班级表"


class CourseANDSubject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="所属课程类型")

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="学科")

    subject_time = models.SmallIntegerField(default=0, verbose_name="课时")

    priority = models.IntegerField(max_length=10, verbose_name="上课顺序")

    def __str__(self):
        return f"{self.course},{self.subject},{self.subject_time},{self.priority}"

    class Meta:
        verbose_name_plural = verbose_name = "课程——学科表"


class Teacher(models.Model):
    TEACHING_CHOICES = (
        (1, '是'),
        (2, '否')
    )

    name = models.CharField(max_length=20, verbose_name="教师")

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="科目")

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="所属课程")


    #老师是否安排课，1是已经安排课了，2是还没有安排课
    teaching = models.IntegerField(verbose_name="是否安排课",choices=TEACHING_CHOICES,default=2)

    def __str__(self):
        return f'{self.name}({self.subject},{self.course})'

    class Meta:
        verbose_name_plural = verbose_name = "教师表"


class ClassTimeTable(models.Model):
    classname = models.CharField(max_length=20, verbose_name="班级名")
    classcourse = models.CharField(max_length=20, verbose_name="课程名")
    classsubjecttime = models.CharField(max_length=20, verbose_name="课时")
    classsubday = models.CharField(max_length=50, verbose_name="上课时间")
    classteacher = models.CharField(max_length=20, verbose_name="教师")
    classtime = models.CharField(max_length=50, verbose_name="上课时间段")

    def __str__(self):
        return f'{self.classname}'

    class Meta:
        verbose_name_plural = verbose_name = "班级课程表"


def get_join_time_by_clid(cl_id):
    join_time = ClassName.objects.filter(id=cl_id)[0].join_time

    return join_time


# 得到总课时数 单位：天
def get_time_table_by_subid(claid):
    subjecttimes = ClassName.objects.get(pk=claid).course.courseandsubject_set.filter(
        course_id=ClassName.objects.filter(pk=claid)[0].course_id)

    subtimecount = 0
    for subtime in subjecttimes:
        subtimecount += subtime.subject_time

    subtimecount = int(subtimecount / 6)
    return subtimecount


# 得到一个总课时的日期列表，排课时间段从该列表中获取
def deal_time(classid, subtimecount):
    jointime = get_join_time_by_clid(classid)
    date_li = [jointime]
    # 得到当前周几
    weekday = jointime.weekday()

    # 从当前周几到本周末还有多少天，并且加到时间列表中
    for _ in range(4 - int(weekday)):
        jointime += datetime.timedelta(days=1)
        date_li.append(jointime)

    # 从第二个周一一直到总课时结束的时间添加到列表中
    next_monday = date_li[-1] + datetime.timedelta(days=2)
    count = []
    while True:
        next_monday += datetime.timedelta(days=1)
        count.append(next_monday)
        date_li.append(next_monday)
        if len(count) == 5:
            next_monday = date_li[-1] + datetime.timedelta(days=2)
            count.clear()
        if len(date_li) == subtimecount:
            break

    return date_li


#点击生成课表的时候修改老师的teaching。

def changing_teaching(tea_id):
    pass

