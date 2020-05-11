from django.db import models
from django.urls import reverse

from django.core.exceptions import ValidationError
from django.core.validators import validate_email, RegexValidator

import re

def default_email():
    return 'defaultemail@mail.ru'

#simple validation example in a models 
def validate_string(line):
    if re.findall(r'[^a-z,A-Z,а-я,А-Я ]',line):
        raise ValidationError(
            'Invalide value: %(val)s\nMast include only letters',
            code='invalid', 
            params={'val':line})

def validate_phone(str_):
    if re.findall(r'[^0-9]+',str_):
        raise ValidationError('Phone number should contain only numbers')
    
    if len(str_)!=11:
        raise ValidationError('Phone number should contain 11 numbers')

###########################################################
###----------------Модель преподавателя
###########################################################
class Teacher(models.Model):
    PersonnelNumber = models.AutoField(primary_key=True,null=False,
        unique=True,blank=False,db_column='Табельный номер сотрудника',
        help_text='Табельный номер сотрудника - уникальное значение')
    #blank=False - обязательное поле
    FirstName = models.CharField(max_length=20,null=False,blank=False, 
        db_column='Имя преподавателя',validators=[validate_string])
    Patronymic = models.CharField(max_length=20, null=False, 
        db_column='Отчество', blank=False, validators=[validate_string])
    LastName = models.CharField(max_length=20,null=False,blank=False, 
        db_column='Фамилия преподавателя', validators=[validate_string])
    TeacherPosition = models.CharField(max_length=20,null=False, 
        blank=False,db_column='Должность преподавателя',validators=[validate_string])
    PhoneNumber = models.CharField(max_length=11,null=False,unique=True, 
        blank=False, db_column='Номер телефона',validators=[validate_phone])
    Email = models.CharField(max_length=30,null=False, unique=True,
        blank=False, default=default_email(), db_column='email', 
        validators=[validate_email])
    Department = models.CharField(max_length=50, null=False, blank=False, 
        db_column='Кафедра', validators=[validate_string])

    disciplines = models.ManyToManyField('Discipline')
    groups = models.ManyToManyField('GroupInInstitute')
    lecturerooms = models.ManyToManyField('LectureRoom')
    calendars = models.ManyToManyField('Calendar')
    pairs = models.ManyToManyField('Pair')

    objects=models.Manager()

    def __str__(self):
        return '{} {}'.format(self.FirstName, self.LastName)

    def get_absolute_url(self):
        #return reverse("university_timetable.views.teacher", kwargs={"pk": self.pk})
        return "/university_timetable/teachers/%i/" % self.pk

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural='Преподаватели'
        #unique_together=('FirstName', 'Patronymic', 'LastName', 'PhoneNumber')

###########################################################
###----------------Модель пары
###########################################################
class Pair(models.Model):
    PairNumber = models.AutoField(primary_key=True, db_column='Номер пары', help_text='help_text')
    PairStart = models.TimeField(null=False, blank=False, db_column='Время начала пары')
    PairStop = models.TimeField(null=False, blank=False, db_column='Время окончания пары')

    objects=models.Manager()

    def __str__(self):
        return '{}'.format(self.PairNumber)

    def get_absolute_url(self):
        return reverse("university_timetable.views.pair", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Пара'
        verbose_name_plural='Пары'

###########################################################
###----------------Модель дисциплины
###########################################################
class Discipline(models.Model):
    Id=models.AutoField(db_column='Код дисциплины',primary_key=True, 
        verbose_name="Код дисциплины")
    Name = models.CharField(db_column='Название дисциплины',
        max_length=60, null=False, verbose_name="Название дисциплины",
        validators=[validate_string])
    AcademicHours = models.IntegerField( 
        db_column='Количество академических часов', 
        null=False, default=0,verbose_name='Количество академических часов',)
    IntermediateCertificationForm = models.CharField(max_length=20,
        db_column='Форма промежуточной аттестации',null=False, 
        default='',choices={('экз', 'экзамен'),
                            ('з', 'зачет'),
                            ('зо', 'зачет с оценкой')},
        verbose_name="Форма промежуточной аттестации")

    objects=models.Manager()

    def __str__(self):
        return '{}'.format(self.Name)

    def get_absolute_url(self):
        return reverse("university_timetable.views.discipline", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural='Дисциплины'

###########################################################
###----------------Модель группы
###########################################################
class GroupInInstitute(models.Model):
    Id=models.AutoField(
                        #db_column='Код группы', 
                        primary_key=True, 
                        verbose_name="Код группы")
    GroupName = models.CharField(max_length=15, validators=[RegexValidator(regex=r'[^a-z,A-Z,а-я,А-Я, ,0-9,-]', message='Некорректное название группы', inverse_match=True)])
    NumberOfPeople = models.IntegerField(null=False, db_column='Количество человек в группе')
    Institute = models.CharField(max_length=60, null=False, db_column='Институт', validators=[validate_string])
    Specialty = models.CharField(max_length=60, null=False, db_column='Специальность', validators=[validate_string])
    FormOfTraining = models.CharField(max_length=12, null=False, db_column='Форма обучения', choices={
        ('о','очная'), ('з','заочная'),('оз','очно-заочная')})
    SemesterNumber = models.IntegerField(null=False, db_column='Номер семестра')
    CourseNumber = models.IntegerField(null=False, db_column='Номер курса')

    pairs = models.ManyToManyField('Pair')
    calendars = models.ManyToManyField('Calendar')
    lecturerooms = models.ManyToManyField('LectureRoom')
    disciplines = models.ManyToManyField('Discipline')
    #plane=models.OneToOneField('AcademicPlan',on_delete=models.CASCADE)

    objects=models.Manager()

    def __str__(self):
        return '{}'.format(self.GroupName)

    def get_absolute_url(self):
        return reverse("university_timetable.views.group", kwargs={"pk": self.pk})


    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural='Группы'

#TODO: скорее всего убрать академический план
###########################################################
###----------------Модель академического плана
###########################################################
# class AcademicPlan(models.Model):
#    id = models.AutoField(primary_key=True, db_column='Код академического плана')

#    disciplines = models.ManyToManyField(Discipline, related_name='academicplan')

#    objects=models.Manager()
   
#    def __str__(self):
#        return "Академический план № {}".format(self.id)


#    class Meta:
#         verbose_name = 'Академический план'
#         verbose_name_plural='Академические планы'

###########################################################
###----------------Модель корпуса
###########################################################
class Building(models.Model):
    NumberOfBuilding = models.IntegerField(primary_key=True, db_column='Номер корпуса')
    Address = models.CharField(max_length=30, null=False, db_column='Адрес корпуса')

    objects=models.Manager()

    def __str__(self):
        return '{}'.format(self.NumberOfBuilding)

    # def get_absolute_url(self):
    #     return reverse("university_timetable.views.building_rooms", kwargs={"pk": self.pk})
    #     #return "/university_timetable/buildings/%i/" % self.NumberOfBuilding

    class Meta:
        verbose_name = 'Корпус'
        verbose_name_plural='Корпуса'

###########################################################
###----------------Модель аудитории
###########################################################
class LectureRoom(models.Model):
    LectureRoomNumber = models.IntegerField(primary_key=True, db_column='Номер аудитории')
    Capacity = models.IntegerField(null=False, db_column='Вместимость аудитории')
    NumberOfBuilding = models.ForeignKey(Building, on_delete=models.CASCADE, to_field='NumberOfBuilding', related_name='lecturerooms')

    objects=models.Manager()

    def __str__(self):
        return '{}'.format(self.LectureRoomNumber)

    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural='Аудитории'

class Calendar(models.Model):
    Id = models.AutoField(primary_key=True)
    TypeOfWeek = models.CharField(max_length=2, null=False, choices={('чн', 'четная'),('нч','нечетная')})
    DayOfWeek = models.CharField(max_length=11, null=False, choices={
        ('пон', 'Понедельник'),
        ('вт', 'Вторник'),
        ('ср', 'Среда'),
        ('чет', 'Четверг'),
        ('пят', 'Пятница'),
        ('суб', 'Суббота'),
        ('вос','Воскресенье')
    })


    objects=models.Manager()

    class Meta:
        verbose_name = 'Календарь'
        verbose_name_plural='Календари'

    def __str__(self):
        return "{} {}".format(self.TypeOfWeek, self.DayOfWeek)