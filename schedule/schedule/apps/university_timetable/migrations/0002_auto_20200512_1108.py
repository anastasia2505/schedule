# Generated by Django 3.0.6 on 2020-05-12 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university_timetable', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='DayOfWeek',
            field=models.CharField(choices=[('суб', 'Суббота'), ('пон', 'Понедельник'), ('чет', 'Четверг'), ('пят', 'Пятница'), ('ср', 'Среда'), ('вос', 'Воскресенье'), ('вт', 'Вторник')], max_length=11),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='IntermediateCertificationForm',
            field=models.CharField(choices=[('з', 'зачет'), ('зо', 'зачет с оценкой'), ('экз', 'экзамен')], db_column='Форма промежуточной аттестации', default='', max_length=20, verbose_name='Форма промежуточной аттестации'),
        ),
    ]
