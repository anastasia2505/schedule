from django.forms import ModelForm
from .models import *
from django.core import validators

class TeacherForm(ModelForm):
    class Meta:
        model=Teacher
        fields=['FirstName', 'Patronymic','LastName','TeacherPosition','Department','PhoneNumber','Email',
                'disciplines','groups','lecturerooms','calendars','pairs']


    def clean(self):
        super(TeacherForm,self).clean()

        if Teacher.objects.filter(FirstName=self.cleaned_data['FirstName'], Patronymic=self.cleaned_data['Patronymic'], LastName=self.cleaned_data['LastName']):
            pass
            
class DisciplineForm(ModelForm):
    class Meta:
        model=Discipline
        fields=['Name', 'AcademicHours', 'IntermediateCertificationForm'] 

    def clean(self):
        super().clean()
        
        if Discipline.objects.filter(Name__iexact=self.cleaned_data['Name'], \
                                AcademicHours=self.cleaned_data['AcademicHours'], \
                                IntermediateCertificationForm=self.cleaned_data['IntermediateCertificationForm']).exists():
            msg_error='Дисциплина уже существует в базе данных'
            self.add_error(None,msg_error)

        
        return self.cleaned_data


class PairForms(ModelForm):
    class Meta:
        model=Pair
        fields=['PairStart', 'PairStop']
        #field=[str(f.name) for f in Pair._meta.get_all_field_names()]s

