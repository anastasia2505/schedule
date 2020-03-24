from django.urls import path, include
from . import views

app_name='university_timetable'
urlpatterns = [
    path('groups/', views.groups, name='groups'),
    path('teachers/', views.teachers, name='teachers'),
    path('disciplines/', views.disciplines, name = 'disciplines'),
    #path('buildings/', views.buildings, name='buildings'),

    path('lecturerooms/', views.lecturerooms, name='lecturerooms'),
    path('pairs/', views.pairs, name='pairs'),
    path('calendars/', views.calendars, name='calendars'),

    path('teachers/<int:teacher_id>/', views.teacher, name='teacher'),
    path('buildings/<int:numb>/', views.building_rooms, name='buildings'),
    path('disciplines/<int:discipline_id>', views.discipline, name='discipline'),
]