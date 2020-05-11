from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from university_timetable.models import *
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.views import View
from django.shortcuts import get_object_or_404


from university_timetable.forms import *
from django.forms.models import modelform_factory
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, csrf_exempt
#from django.core.context_processors import csrf

class GroupsView(View):

    def get(self, request):
        groups_list=GroupInInstitute.objects.all().order_by('GroupName')
        return render(request,'university_timetable/group/index_groups.html',context={'groups_list':groups_list})



class TeacherView(View):

    
    def get(self, request, teacher_id=None):
        if teacher_id:
            try:
                # cur_teacher = Teacher.objects.get(pk=teacher_id)
                # list_disciplines = list(cur_teacher.disciplines.all().order_by('Name'))
                # list_groups = list(cur_teacher.groups.all().order_by('GroupName'))
                # list_pairs = list(cur_teacher.pairs.all().order_by('PairNumber'))
                # list_lecturerooms = list(cur_teacher.lecturerooms.all().order_by('LectureRoomNumber'))
                #list_buildings = list(temp.NumberOfBuilding.objects.order_by('NumberOfBuilding').distinct(
                #    'NumberOfBuilding') for temp in cur_teacher.lecturerooms.all())
                teacher=get_object_or_404(Teacher, pk=teacher_id)
                form=TeacherForm(instance=teacher)
            except Teacher.DoesNotExist:
                raise Http404("Преподаватель не найден")
            return render(request, 'university_timetable/teacher/teacher_detail.html',
                    context={'form': form,
                            'cur_teacher': teacher})
        else:
            teachers_list = Teacher.objects.all()
            return render(request, 'university_timetable/teacher/index_teachers.html', context={'teaches_list': teachers_list,})

    @staticmethod
    def create(request):
        if request.method=="GET":
            form=TeacherForm()
            return render(request, 'university_timetable/teacher/create.html', context={'form':form,})
        
        if request.method=="POST":
            data_form=TeacherForm(request.POST)

            if data_form.is_valid():
                teacher=Teacher.objects.create(
                    FirstName=request.POST.get('FirstName'),
                    Patronymic=request.POST.get('Patronymic'),
                    LastName=request.POST.get('LastName'),
                    TeacherPosition=request.POST.get('TeacherPosition'),
                    PhoneNumber=request.POST.get('PhoneNumber'),
                    Email=request.POST.get('Email'),
                    Department=request.POST.get('Department'),
                )
                teacher.disciplines.add(request.POST.get('disciplines'))
                teacher.groups.add(request.POST.get('groups'))
                teacher.lecturerooms.add(request.POST.get('lecturerooms'))
                teacher.calendars.add(request.POST.get('calendars'))
                teacher.pairs.add(request.POST.get('pairs'))
                teacher.save()
            return HttpResponseRedirect(reverse('university_timetable:teachers'))

    @staticmethod
    def update(request, teacher_id):
        
        if request.method=='GET':
            cur_teacher=get_object_or_404(Teacher, pk=teacher_id)
            form=TeacherForm(instance=cur_teacher)
            return render(request, 'university_timetable/teacher/update.html',
                    context={'form': form,
                            'cur_teacher': cur_teacher})

        if request.method=='POST':
            data_form=TeacherForm(request.POST)
            
            #product.name = 'Name changed again'
            #product.save(update_fields=['name'])
            if data_form.is_valid():
                teacher=Teacher.objects.get(pk=teacher_id)
                
                teacher.FirstName=request.POST.get('FirstName')
                teacher.Patronymic=request.POST.get('Patronymic')
                teacher.LastName=request.POST.get('LastName')
                teacher.TeacherPosition=request.PUPOSTT.get('TeacherPosition')
                teacher.PhoneNumber=request.POST.get('PhoneNumber')
                teacher.Email=request.POST.get('Email')
                teacher.Department=request.POST.get('Department')
                
                teacher.disciplines.add(request.POST.get('disciplines'))
                teacher.groups.add(request.POST.get('groups'))
                teacher.lecturerooms.add(request.POST.get('lecturerooms'))
                teacher.calendars.add(request.POST.get('calendars'))
                teacher.pairs.add(request.POST.get('pairs'))

                teacher.save(force_update=True)
            return HttpResponseRedirect(reverse('university_timetable:teacher', args=(teacher_id,)))

    #@ensure_csrf_cookie
    #@csrf_exempt  
    def delete(self, request, teacher_id):

        try:
            person=Teacher.objects.get(pk=teacher_id)
            person.delete()
        except ObjectDoesNotExist:
            raise Http404("Преподаватель не найден")

        return render(request, 'university_timetable/teacher/index_teachers.html', context={'teacher_list': Teacher.objects.all()})

class DisciplineView(View):

    def get(self, request, discipline_id=None):
        if discipline_id:
            try:
                cur_discipline = Discipline.objects.get(pk=discipline_id)
                disciplineform=DisciplineForm(instance=cur_discipline)

            except Discipline.DoesNotExist:
                raise Http404("Дисциплина не найдена")
            return render(request, 'university_timetable/discipline/discipline_detail.html', context={'form':disciplineform, 'cur_discipline':cur_discipline})
        else:
            disciplines_list=Discipline.objects.all()
            return render(request,'university_timetable/discipline/index_disciplines.html',context={'disciplines_list':disciplines_list})
    
    @staticmethod
    def create(request):
        if request.method=='GET':
            form=DisciplineForm()
            return render(request, 'university_timetable/discipline/create.html', context={'form':form,})

        if request.method=='POST':
            form=DisciplineForm(request.POST)
            if form.is_valid():
                discipline=Discipline.objects.create(Name=request.POST.get('Name'),
                                                AcademicHours=request.POST.get('AcademicHours'),
                                                IntermediateCertificationForm=request.POST.get('IntermediateCertificationForm'))
            
            return HttpResponseRedirect(reverse('university_timetable:disciplines'))
    
    #@ensure_csrf_cookie
    #@staticmethod
    def delete(self, request, discipline_id):
        try:
            Discipline.objects.get(pk=discipline_id).delete()
        except Discipline.DoesNotExist:
            raise Http404('Дисциплина не найдена')
        return render(request, 'university_timetable/discipline/index_disciplines.html', context={'disciplines_list': Discipline.objects.all()})

    
    @staticmethod
    def update(request, discipline_id):
        if request.method=='GET':
            cur_discipline=get_object_or_404(Discipline, pk=discipline_id)
            form=DisciplineForm(instance=cur_discipline)
            return render(request, 'university_timetable/discipline/update.html', context={'form':form,
                                                                                            'cur_discipline': cur_discipline})
        if request.method=='PUT':
            discipline=get_object_or_404(Discipline, pk=discipline_id)
            data_form=DisciplineForm(initial=request.PUT, instance=discipline)
            
            if data_form.is_valid():
                discipline.Name=request.PUT.get('Name')
                discipline.AcademicHours=request.PUT.get('AcademicHours')
                discipline.IntermediateCertificationForm=request.PUT.get('IntermediateCertificationForm')
                discipline.save()
                
            #TODO:исправить переадресацию
            return HttpResponseRedirect(reverse('university_timetable:discipline', args=(discipline_id,)))


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

class LectureroomView(View):

    def get(self, request, lectureroom_id=None):
        if lectureroom_id:
            pass
        else:    
            lecturerooms_list=LectureRoom.objects.all()
            return render(request,'university_timetable/index_lecturerooms.html',context={'lecturerooms_list':lecturerooms_list})

class PairView(View):
    #шаблона нет
    def get(self, request, pair_id=None):
        if pair_id:
            pass
        else:
            pairs_list=Pair.objects.all()
            return render(request,'university_timetable/index_pairs.html',context={'pairs_list':pairs_list})

class CalendarView(View):

    def get(self, request, calendar_id=None):
        if calendar_id:
            pass
        else:        
            calendars_list=Calendar.objects.all()
            return render(request, 'university_timetable/index_calendars.html', context={'calendars_list': calendars_list})


def my_custom_page_not_found_view(request, exception):
    render(request, 'university_timetable/404.html')

class StartView(View):

    def get(self, request, group_name=None):
        if group_name:
            try:
                groups_list = GroupInInstitute.objects.all().order_by('GroupName')
                pair_list_group = GroupInInstitute.objects.get(GroupName=groups_list[group_name]).pairs.all()
                teacher_list = Teacher.objects.all().filter(groups__GroupName=groups_list[group_name])
                data = {"groups_list": groups_list,
                        "pair_list_group": pair_list_group,
                        "gp":gp,
                        "teacher_list": teacher_list}
            except GroupInInstitute.DoesNotExist:
                raise Http404("Группа не найдена")
            return render(request, 'university_timetable/timetable/timetable_detail.html', context=data)
        else:
            group_list = GroupInInstitute.objects.all()
            return render(request, 'university_timetable/timetable/timetable_index.html', context={'group_list': group_list})

