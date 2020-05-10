from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='university_timetable'#пространство имен
urlpatterns = [   
    #Groups
    path('groups/', views.GroupView.as_view(), name='groups'),
    path('groups/<int:pk>/', views.GroupView.as_view(), name='group'),
    path('groups/create/', views.GroupView.create, name='group_create'),
    path('groups/<int:pk>/update/', views.GroupView.update, name='group_update'),

    #LectureRooms
    path('lecturerooms/', views.LectureroomView.as_view(), name='lecturerooms'),
    path('lecturerooms/<int:pk>/', views.LectureroomView.as_view(), name='lectureroom'),
    path('lecturerooms/create/', views.LectureroomView.create, name='lectureroom_create'),
    path('lecturerooms/<int:pk>/update/', views.LectureroomView.update, name='lectureroom_update'),

    path('pairs/', views.PairView.as_view(), name='pairs'),
    path('calendars/', views.CalendarView.as_view(), name='calendars'),
    
    #Teachers
    path('teachers/', views.TeacherView.as_view(), name='teachers'),
    path('teachers/create/', views.TeacherView.create, name="teacher_create"),
    path('teachers/<int:teacher_id>/', views.TeacherView.as_view(), name='teacher'),
    path('teachers/<int:teacher_id>/update/', views.TeacherView.update, name='teacher_update'),
    
    #Disciplines
    path('disciplines/', views.DisciplineView.as_view(), name = 'disciplines'),
    path('disciplines/<int:discipline_id>/', views.DisciplineView.as_view(), name='discipline'),
    path('disciplines/create/', views.DisciplineView.create, name='discipline_create'),
    path('disciplines/<int:discipline_id>/update/', views.DisciplineView.update, name='discipline_update'),

    #Buildings
    path('buildings/<int:pk>/', views.BuildingView.as_view(), name='building'),
    path('buildings/', views.BuildingView.as_view(), name = 'buildings'),
    path('buildings/create/', views.BuildingView.create, name='building_create'),
    path('buildings/<int:pk>/update/', views.BuildingView.update, name='building_update'),
    ] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    