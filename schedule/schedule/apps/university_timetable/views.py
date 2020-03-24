from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import *
from django.core.exceptions import ObjectDoesNotExist

def groups(request):

    groups_list=GroupInInstitute.objects.all()
    return render(request,'university_timetable/index_groups.html',context={'groups_list':groups_list})

def teachers(request):
    try:
        teachers_list = Teacher.objects.all()
        #disc={cur_teacher.PersonnelNumber: list(cur_teacher.disciplines.all().order_by('Name')) for cur_teacher in teachers_list}
    except Teacher.DoesNotExist:
        raise Http404("Opps")
    return render(request, 'university_timetable/index_teachers.html', context={'teaches_list': teachers_list,})

def teacher(request, teacher_id):
    try:
        cur_teacher = Teacher.objects.get(pk=teacher_id)
        list_disciplines = list(cur_teacher.disciplines.all().order_by('Name'))
        list_groups = list(cur_teacher.groups.all().order_by('GroupName'))
        list_pairs = list(cur_teacher.pairs.all().order_by('PairNumber'))
        list_lecturerooms = list(cur_teacher.lecturerooms.all().order_by('LectureRoomNumber'))
        #list_buildings = list(temp.NumberOfBuilding.objects.order_by('NumberOfBuilding').distinct(
        #    'NumberOfBuilding') for temp in cur_teacher.lecturerooms.all())

    except Teacher.DoesNotExist:
        raise Http404("Преподаватель не найден")
    return render(request, 'university_timetable/teacher_detail.html',
            context={'cur_teacher': cur_teacher,
            'list_disciplines': list_disciplines,
            'list_groups': list_groups,
            'list_pairs': list_pairs,
            'list_lecturerooms':list_lecturerooms})


def disciplines(request):
    disciplines_list=Discipline.objects.all()
    return render(request,'university_timetable/index_disciplines.html',context={'disciplines_list':disciplines_list})

def discipline(request, discipline_id):
    try:
        cur_discipline = Discipline.objects.get(pk=discipline_id)
        academ_plan = cur_discipline.academicplan
    except Discipline.DoesNotExist:
        raise Http404("Дисциплина не найдена")
    return render(request, 'university_timetable/discipline_detail.html', context={'discipline':cur_discipline, 'academ_plan': academ_plan})



def building_rooms(request, numb):
    buildings_list = Building.objects.all()
    try:
        cur_building=Building.objects.get(NumberOfBuilding=numb)
        lec_rooms_list = cur_building.lectureroom_set.order_by('-NumberOfBuilding')
        context={'cur_build':cur_building, 'lrooms_list' : lec_rooms_list}
    except:
        print('Ошибка')
        context={'cur_build':cur_building}
    finally:
        return render(request,'university_timetable/index_building_rooms.html',context=context)

def lecturerooms(request):
    lecturerooms_list=LectureRoom.objects.all()
    return render(request,'university_timetable/index_lecturerooms.html',context={'lecturerooms_list':lecturerooms_list})

#шаблона нет
def pairs(request):
    pairs_list=Pair.objects.all()
    return render(request,'university_timetable/index_pairs.html',context={'pairs_list':pairs_list})

def calendars(request):
    calendars_list=Calendar.objects.all()
    return render(request, 'university_timetable/index_calendars.html', context={'calendars_list': calendars_list})


def my_custom_page_not_found_view(request, exception):
    render(request, 'university_timetable/404.html')