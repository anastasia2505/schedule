from django.forms import ModelForm, NullBooleanField, ValidationError
from .models import Teacher, Discipline, Pair, GroupInInstitute, LectureRoom, Building, Calendar
from django.core import validators
from django.utils.translation import ugettext_lazy as _ 

class TeacherForm(ModelForm):
    class Meta:
        model=Teacher
        fields=['FirstName', 'Patronymic','LastName','TeacherPosition','Department','PhoneNumber','Email',
                'disciplines','groups','lecturerooms','calendars','pairs']
            
class DisciplineForm(ModelForm):
    class Meta:
        model=Discipline
        fields=['Name', 'AcademicHours', 'IntermediateCertificationForm'] 

    def clean_AcademicHours(self):
        data=self.cleaned_data.get('AcademicHours')
        if data not in range(90,300):
            #self._errors["AcademicHours"] = self.error_class(['Invalid value AcademicHours'])
            raise ValidationError(_('Invalid value AcademicHours: %(value)s'),
                code='invalid',
                params={'value': data},)

        return self.cleaned_data.get('AcademicHours')
    
class PairForms(ModelForm):
    class Meta:
        model=Pair
        fields=['PairStart', 'PairStop']

class LectureRoomForm(ModelForm):
    class Meta:
        model=LectureRoom
        fields='__all__' 

    #Teachers=NullBooleanField()
    
    def clean_LectureRoomNumber(self):
        data=self.cleaned_data.get('LectureRoomNumber')
        if len(str(data))!=4:
            raise ValidationError(_('некорректный номер аудитории: %(value)s (должен содержать 4 цифры)'),
                code='invalid',
                params={'value': data},)

        if int(str(data)[1]) not in range(1,6):
            raise ValidationError(_('некорректный номер аудитории: %(value)s (максимум 5 этажей)'),
                code='invalid',
                params={'value': data},)

        return data

    def clean_Capacity(self):
        data=self.cleaned_data.get('Capacity')
        if data not in range(15,101):
            raise ValidationError(_('Некорректное значение вместимости аудитории: %(value)s (допустимые значения 15-100)'),
                code='invalid',
                params={'value': data},)
        
        return data


    def clean(self):
        cleaned_data=super().clean()
        
        lecture_room=cleaned_data.get('LectureRoomNumber')
        building=cleaned_data.get('Building')

        if lecture_room and building and lecture_room//1000!=building.NumberOfBuilding:
            raise ValidationError(_('Некорректный ввод, 1 цифра номера аудитории должна совпадать с номером корпуса'))
                
        # if LectureRoom.objects.filter('')
        #     msg_error=''
        #     self.add_error(None,msg_error)

        return cleaned_data

class BuildingForm(ModelForm):
    class Meta:
        model=Building
        fields='__all__' 
        

    def clean_NumberOfBuilding(self):
        data=self.cleaned_data.get('NumberOfBuilding')

        if data not in range(1,7):
            raise ValidationError(_('Некорректное номер корпуса: %(value)s (допустимые значения 1-6)'),
                code='invalid',
                params={'value': data},)

        return self.cleaned_data

class GroupForm(ModelForm):
    class Meta:
        model=GroupInInstitute
        fields='__all__' 

    def clean_NumberOfPeople(self):
        data=self.cleaned_data.get('NumberOfPeople')
        if data not in range(1,41):
            raise ValidationError(_('Некорректное количество человек в группе: %(value)s (диапазон 1-40)'),
                code='invalid',
                params={'value': data},)
        return data
    
    def clean_SemesterNumber(self):
        data=self.cleaned_data.get('SemesterNumber')

        if data not in range(1,11):
            raise ValidationError(_('Некорректное значение семестра: %(value)s (диапазон 1-10)'),
                code='invalid',
                params={'value': data},)
        return data

    def clean_CourseNumber(self):
        data=self.cleaned_data.get('CourseNumber')

        if data not in range(1,6):
            raise ValidationError(_('Некорректное значение номера курса: %(value)s (диапазон 1-5)'),
                code='invalid',
                params={'value': data},)
        return data

    def clean(self):
        cleaned_data=super().clean()
        if cleaned_data.get('CourseNumber') and cleaned_data.get('SemesterNumber'):
            values={'1': [1,2],
                    '2': [3,4],
                    '3': [5,6],
                    '4': [7,8],
                    '5': [9,10]}
            if cleaned_data.get('SemesterNumber') not in values.get(str(cleaned_data.get('CourseNumber'))):
                raise ValidationError(_('Несоответствие номера курса и номера семестра'))
                    

        return cleaned_data
class CalendarForm(ModelForm):
    class Meta:
        model=Calendar
        fields='__all__'