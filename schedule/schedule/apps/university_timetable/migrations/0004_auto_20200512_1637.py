# Generated by Django 3.0.6 on 2020-05-12 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university_timetable', '0003_auto_20200512_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='DayOfWeek',
            field=models.CharField(choices=[('чет', 'Четверг'), ('вт', 'Вторник'), ('пон', 'Понедельник'), ('пят', 'Пятница'), ('ср', 'Среда'), ('суб', 'Суббота'), ('вос', 'Воскресенье')], max_length=11),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='IntermediateCertificationForm',
            field=models.CharField(choices=[('экз', 'экзамен'), ('зо', 'зачет с оценкой'), ('з', 'зачет')], db_column='Форма промежуточной аттестации', default='', max_length=20, verbose_name='Форма промежуточной аттестации'),
        ),
        migrations.AlterField(
            model_name='groupininstitute',
            name='FormOfTraining',
            field=models.CharField(choices=[('оз', 'очно-заочная'), ('з', 'заочная'), ('о', 'очная')], db_column='Форма обучения', max_length=12),
        ),
    ]