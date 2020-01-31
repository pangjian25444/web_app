from django.shortcuts import render

# Create your views here.


from .models import *

app_name = 'course_app'

def index(request):
    class_li = ClassName.objects.all()
    course_li = Course.objects.all()
    return render(request, "course_app/index.html", locals())


def add(request, id):
    course_order_li = CourseANDSubject.objects.filter(course_id=ClassName.objects.filter(pk=id)[0].course_id).order_by(
        'priority')
    classname_name = ClassName.objects.filter(pk=id)[0].name
    classname_id = id
    count = -1

    return render(request, "course_app/add_timetable.html", locals())


def save_info(request, id):
    classcourse = request.POST.getlist('classcourse')
    classsubjecttime = request.POST.getlist('classsubjecttime')
    classsubday = request.POST.getlist('classsubday')
    classteacher = request.POST.getlist('classteacher')
    classtime = request.POST.getlist('classtime')

    classname_name = ClassName.objects.filter(pk=id)[0].name

    if ClassTimeTable.objects.filter(classname=classname_name):
        return render(request, "course_app/save_fail.html")

    else:

        for i in range(len(classcourse)):
            Teacher.objects.filter(name=classteacher[i]).update(teaching=1)

            ClassTimeTable.objects.create(classname=classname_name, classcourse=classcourse[i],
                                          classsubjecttime=classsubjecttime[i], classsubday=classsubday[i],
                                          classteacher=classteacher[i], classtime=classtime[i])

    return render(request, "course_app/save_into.html", locals())


def search(request, name):
    time_table = ClassTimeTable.objects.filter(classname=name).all()
    classname_name = name
    return render(request, "course_app/search.html", locals())
