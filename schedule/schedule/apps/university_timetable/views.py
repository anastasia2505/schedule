from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Teacher, Discipline, GroupInInstitute, Pair, Calendar, LectureRoom, Building
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.views import View
from django.shortcuts import get_object_or_404


from university_timetable.forms import *
from django.forms.models import modelform_factory
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, csrf_exempt
#from django.core.context_processors import csrf

class GroupView(View):

    def get(self, request, pk=None):
        if pk:
            try:
                instance=GroupInInstitute.objects.get(pk=pk)
                #способ инициализации form(data={some data}, instance=instance) не работает, поэтому прописываю вручную
                data={'GroupName': instance.GroupName,
                    'NumberOfPeople': instance.NumberOfPeople,
                    'Institute': instance.Institute,
                    'Specialty':instance.Specialty,
                    'FormOfTraining': instance.FormOfTraining,
                    'SemesterNumber':instance.SemesterNumber,
                    'CourseNumber':instance.CourseNumber,
                    'pairs':instance.pairs.all(),
                    'calendars':instance.calendars.all(),
                    'lecturerooms': instance.lecturerooms.all(),
                    'disciplines':instance.disciplines.all(),
                    'teachers':instance.teacher_set.all()}
                form=GroupForm(data)
            except GroupInInstitute.DoesNotExist:
                raise Http404("Группа {} не найдена".format(pk))
            return render(request, 'university_timetable/group/group_detail.html', context={'form':form, 'group': instance})
        else:    
            def default():
                return GroupInInstitute.objects.all().order_by('GroupName')
            
            def reverse():
                return GroupInInstitute.objects.all().order_by('-GroupName')
            
            filters={'default': default,
                    'reverse': reverse,}
            
            filter=request.GET.get('filter', 'default')
            list_=filters.get(filter)

            return render(request,'university_timetable/group/index_groups.html',context={'group_list':list_})

    def delete(self, request, pk=None):
        try:
            instance=GroupInInstitute.objects.get(pk=pk)
            instance.delete()
        except GroupInInstitute.DoesNotExist:
            raise Http404("Группа {} не найдена".format(pk))
        return render(request, 'university_timetable/group/index_groups.html', context={'group_list': GroupInInstitute.objects.all()})
    
    @staticmethod
    def create(request):
        if request.method=='GET':
            form=GroupForm()
            return render(request, 'university_timetable/group/create.html', context={'form':form,})
        if request.method=='POST':
            form=GroupForm(request.POST)
            if form.is_valid():
                instance=form.save()
                for elem in form.cleaned_data.get('teachers'):
                    instance.teacher_set.add(elem)
                return HttpResponseRedirect(reverse('university_timetable:groups', args=()))
            else:
                return render(request, 'university_timetable/group/create.html', context={'form':form,})

    @staticmethod
    def update(request, pk=None):
        if request.method=='GET':
            instance=get_object_or_404(GroupInInstitute, pk=pk)
            data={'GroupName': instance.GroupName,
                    'NumberOfPeople': instance.NumberOfPeople,
                    'Institute': instance.Institute,
                    'Specialty':instance.Specialty,
                    'FormOfTraining': instance.FormOfTraining,
                    'SemesterNumber':instance.SemesterNumber,
                    'CourseNumber':instance.CourseNumber,
                    'pairs':instance.pairs.all(),
                    'calendars':instance.calendars.all(),
                    'lecturerooms': instance.lecturerooms.all(),
                    'disciplines':instance.disciplines.all(),
                    'teachers':instance.teacher_set.all()}
            form=GroupForm(data)
            return render(request, 'university_timetable/group/update.html', context={'form':form,
                                                                                            'group': instance})
        if request.method=='POST':
            update_instance=get_object_or_404(GroupInInstitute, pk=pk)
            form=GroupForm(request.POST, instance=update_instance)
            
            if form.is_valid():
                update_instance=form.save()
                for elem in form.cleaned_data.get('teachers'):
                    update_instance.teacher_set.add(elem)
                return HttpResponseRedirect(reverse('university_timetable:groups', args=()))

            return render(request, 'university_timetable/group/update.html', context={'form':form,
                                                                                        'group': update_instance})        



class TeacherView(View):

    
    def get(self, request, teacher_id=None):
        if teacher_id:
            try:
                teacher=get_object_or_404(Teacher, pk=teacher_id)
                form=TeacherForm(instance=teacher)
            except Teacher.DoesNotExist:
                raise Http404("Преподаватель не найден")
            return render(request, 'university_timetable/teacher/teacher_detail.html',
                    context={'form': form,
                            'cur_teacher': teacher})
        else:  
            
            def default():
                return Teacher.objects.all().order_by('FirstName', 'Patronymic', 'LastName')

            def reverse():
                return Teacher.objects.all().order_by('-FirstName', '-Patronymic', '-LastName')
            

            filters={'default' : default,
                    'reverse' : reverse,}
  
            teachers_list=filters[request.GET.get('filter', 'default')]()

            return render(request, 'university_timetable/teacher/index_teachers.html', context={'teaches_list': teachers_list,})

    @staticmethod
    def create(request):
        if request.method=="GET":
            form=TeacherForm()
            return render(request, 'university_timetable/teacher/create.html', context={'form':form,})
        
        if request.method=="POST":
            data_form=TeacherForm(request.POST)

            #TODO: need to add validationerror(for unique_together fields)
            if data_form.is_valid():
                # teacher=Teacher.objects.create(
                #     FirstName=request.POST.get('FirstName'),
                #     Patronymic=request.POST.get('Patronymic'),
                #     LastName=request.POST.get('LastName'),
                #     TeacherPosition=request.POST.get('TeacherPosition'),
                #     PhoneNumber=request.POST.get('PhoneNumber'),
                #     Email=request.POST.get('Email'),
                #     Department=request.POST.get('Department'),
                # )
                # teacher.disciplines.add(request.POST.get('disciplines'))
                # teacher.groups.add(request.POST.get('groups'))
                # teacher.lecturerooms.add(request.POST.get('lecturerooms'))
                # teacher.calendars.add(request.POST.get('calendars'))
                # teacher.pairs.add(request.POST.get('pairs'))
                # teacher.save()
                data_form.save()
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
            update_instance=get_object_or_404(Teacher, pk=teacher_id)
            data_form=TeacherForm(request.POST, instance=update_instance)
            
            #product.name = 'Name changed again'
            #product.save(update_fields=['name'])
            if data_form.is_valid():
                # teacher=Teacher.objects.get(pk=teacher_id)
                
                # teacher.FirstName=request.POST.get('FirstName')
                # teacher.Patronymic=request.POST.get('Patronymic')
                # teacher.LastName=request.POST.get('LastName')
                # teacher.TeacherPosition=request.PUPOSTT.get('TeacherPosition')
                # teacher.PhoneNumber=request.POST.get('PhoneNumber')
                # teacher.Email=request.POST.get('Email')
                # teacher.Department=request.POST.get('Department')
                
                # teacher.disciplines.add(request.POST.get('disciplines'))
                # teacher.groups.add(request.POST.get('groups'))
                # teacher.lecturerooms.add(request.POST.get('lecturerooms'))
                # teacher.calendars.add(request.POST.get('calendars'))
                # teacher.pairs.add(request.POST.get('pairs'))

                # teacher.save(force_update=True)
                if data_form.has_changed():
                    data_form.save()
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
                data={'teachers':cur_discipline.teacher_set.all(),
                    'groups':cur_discipline.groupininstitute_set.all(),
                    'Name':cur_discipline.Name,
                    'AcademicHours': cur_discipline.AcademicHours,
                    'IntermediateCertificationForm':cur_discipline.IntermediateCertificationForm}
                disciplineform=DisciplineForm(data)

            except Discipline.DoesNotExist:
                raise Http404("Дисциплина не найдена")
            return render(request, 'university_timetable/discipline/discipline_detail.html', context={'form':disciplineform, 'discipline':cur_discipline})
        else:
            disciplines_list=Discipline.objects.all()
            return render(request,'university_timetable/discipline/index_disciplines.html',context={'discipline_list':disciplines_list})
    
    @staticmethod
    def create(request):
        if request.method=='GET':
            form=DisciplineForm()
            return render(request, 'university_timetable/discipline/create.html', context={'form':form,})

        if request.method=='POST':
            form=DisciplineForm(request.POST)
            
            if form.is_valid():
                discipline=form.save()
                for elem in form.cleaned_data.get('teachers'):
                    discipline.teacher_set.add(elem)
                for elem in form.cleaned_data.get('groups'):
                    discipline.groupininstitute_set.add(elem)

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
            data={'teachers':cur_discipline.teacher_set.all(),
                'groups':cur_discipline.groupininstitute_set.all(),
                'Name':cur_discipline.Name,
                'AcademicHours': cur_discipline.AcademicHours,
                'IntermediateCertificationForm':cur_discipline.IntermediateCertificationForm}
            form=DisciplineForm(data)
            return render(request, 'university_timetable/discipline/update.html', context={'form':form,
                                                                                            'discipline': cur_discipline})
        if request.method=='POST':
            discipline=get_object_or_404(Discipline, pk=discipline_id)
            data_form=DisciplineForm(request.POST, instance=discipline)
            
            if data_form.is_valid():
                data_form.save()
                for elem in data_form.cleaned_data.get('teachers'):
                    discipline.teacher_set.add(elem)
                for elem in data_form.cleaned_data.get('groups'):
                    discipline.groupininstitute_set.add(elem)

                # discipline.Name=request.PUT.get('Name')
                # discipline.AcademicHours=request.PUT.get('AcademicHours')
                # discipline.IntermediateCertificationForm=request.PUT.get('IntermediateCertificationForm')
                # discipline.save()
                #discipline.save()
            #TODO:исправить переадресацию
            return HttpResponseRedirect(reverse('university_timetable:discipline', args=(discipline_id,)))

class LectureroomView(View):

    def get(self, request, pk=None):
        if pk:
            try:
                instance=LectureRoom.objects.get(pk=pk)
                form=LectureRoomForm(instance=instance)
            except LectureRoom.DoesNotExist:
                raise Http404("Аудитория {} не найдена".format(pk))
            return render(request, 'university_timetable/lectureroom/lectureroom_detail.html', context={'form':form, 'lectureroom': instance})
        else:    
            def default():
                return LectureRoom.objects.all().order_by('LectureRoomNumber')
            
            def reverse():
                return LectureRoom.objects.all().order_by('-LectureRoomNumber')
            
            filters={'default': default,
                    'reverse': reverse,}
            
            filter=request.GET.get('filter', 'default')
            list_=filters.get(filter)

            return render(request,'university_timetable/lectureroom/index_lecturerooms.html',context={'lecturerooms_list':list_})
    
    #TODO: fix page after deleting an object
    def delete(self, request, pk):
        try:
            LectureRoom.objects.get(pk=pk).delete()
        except:
            raise Http404("Аудитория {} не найдена".format(pk))
        return render(request, 'university_timetable/lectureroom/index_lecturerooms.html', context={'lectureroom_list': LectureRoom.objects.all()})
    
    @staticmethod
    def create(request):
        if request.method=='GET':
            form=LectureRoomForm()
            return render(request, 'university_timetable/lectureroom/create.html', context={'form':form,})
        if request.method=='POST':
            form=LectureRoomForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('university_timetable:lecturerooms', args=()))
            else:
                return render(request, 'university_timetable/lectureroom/create.html', context={'form':form,})

    # def put(self, request, pk):
    #     update_instance=get_object_or_404(LectureRoom, pk=pk)
    #     data_form=LectureRoomForm(request.body)
        
    #     if data_form.is_valid():
    #         update_instance.Capacity=request.body['Capacity']
    #         update_instance.save()
    #         #obj.refresh_from_db()
    #     else: 
    #         return render(request, 'university_timetable/lectureroom/update.html', context={'form':data_form,
    #                                                                                    'lectureroom': update_instance})
    #
    #    return HttpResponseRedirect(reverse('university_timetable:lecturerooms', args=()))

    @staticmethod
    def update(request, pk):
        if request.method=='GET':
            instance=get_object_or_404(LectureRoom, pk=pk)
            form=LectureRoomForm(instance=instance, )
            return render(request, 'university_timetable/lectureroom/update.html', context={'form':form,
                                                                                            'lectureroom': instance})
        if request.method=='POST':
            update_instance=get_object_or_404(LectureRoom, pk=pk)
            data_form=LectureRoomForm(request.POST, instance=update_instance)
            
            if data_form.is_valid():
                #update_instance.Capacity=data_form..get('Capacity')
                #update_instance.save()
                if data_form.has_changed():
                    data_form.save()
                #obj.refresh_from_db()
                #TODO:исправить переадресацию
                return HttpResponseRedirect(reverse('university_timetable:lecturerooms', args=()))
            else: 
                return render(request, 'university_timetable/lectureroom/update.html', context={'form':data_form,
                                                                                            'lectureroom': update_instance})

class BuildingView(View):
    def get(self, request, pk=None):
        if pk:
            try:
                instance=Building.objects.get(pk=pk)
                form=BuildingForm(instance=instance)
            except Building.DoesNotExist:
                raise Http404("Корпус {} не найден".format(pk))
            return render(request, 'university_timetable/building/building_detail.html', context={'form':form, 'building': instance})
        else:    
            def default():
                return Building.objects.all().order_by('NumberOfBuilding')
            
            def reverse():
                return Building.objects.all().order_by('-NumberOfBuilding')
            
            filters={'default': default,
                    'reverse': reverse,}
            
            filter=request.GET.get('filter', 'default')
            list_=filters.get(filter)

            return render(request,'university_timetable/building/index_buildings.html',context={'building_list':list_})

    def delete(self, request, pk=None):
        try:
            instance=Building.objects.get(pk=pk)
            instance.delete()
        except Building.DoesNotExist:
            raise Http404("корпус {} не найден".format(pk))
        return render(request, 'university_timetable/building/index_buildings.html', context={'building_list': Building.objects.all()})
    
    @staticmethod
    def create(request):
        if request.method=='GET':
            form=BuildingForm()
            return render(request, 'university_timetable/building/create.html', context={'form':form,})
        if request.method=='POST':
            form=BuildingForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('university_timetable:buildings', args=()))
            else:
                return render(request, 'university_timetable/building/create.html', context={'form':form,})

    @staticmethod
    def update(request, pk=None):
        if request.method=='GET':
            instance=get_object_or_404(Building, pk=pk)
            form=BuildingForm(instance=instance)
            return render(request, 'university_timetable/building/update.html', context={'form':form,
                                                                                            'building': instance})
        if request.method=='POST':
            update_instance=get_object_or_404(Building, pk=pk)
            form=BuildingForm(request.POST, instance=update_instance)
            
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('university_timetable:buildings', args=()))

            return render(request, 'university_timetable/building/update.html', context={'form':form,
                                                                                        'building': update_instance})
            
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

