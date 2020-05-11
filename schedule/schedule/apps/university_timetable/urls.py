from django.urls import path, include
from . import views

app_name='university_timetable'#пространство имен
urlpatterns = [
    path('', views.StartView.as_view(), name='start_page'),
    path('<int:group_name>/', views.StartView.as_view(), name='timetable_detail'),

    #path('groups/', views.groups, name='groups'),
    path('groups/', views.GroupsView.as_view(), name='groups'),
    

    path('lecturerooms/', views.LectureroomView.as_view(), name='lecturerooms'),
    path('pairs/', views.PairView.as_view(), name='pairs'),
    path('calendars/', views.CalendarView.as_view(), name='calendars'),

    path('teachers/', views.TeacherView.as_view(), name='teachers'),
    path('teachers/create', views.TeacherView.create, name="teacher_create"),
    path('teachers/<int:teacher_id>/', views.TeacherView.as_view(), name='teacher'),
    path('teachers/<int:teacher_id>/update', views.TeacherView.update, name='teacher_update'),
    

    path('disciplines/', views.DisciplineView.as_view(), name = 'disciplines'),
    path('disciplines/<int:discipline_id>/', views.DisciplineView.as_view(), name='discipline'),
    path('disciplines/create', views.DisciplineView.create, name='discipline_create'),
    path('disciplines/<int:discipline_id>/update', views.DisciplineView.update, name='discipline_update'),

    path('buildings/<int:numb>/', views.building_rooms, name='buildings'),
]