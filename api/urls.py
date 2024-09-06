from django.urls import path

from . import views

urlpatterns = [
    path('school/create', views.add_school, name='add-school'),
    path('school/all', views.get_all_school, name='view_school'),
    path('school/list', views.get_schools, name='view_schools'),
    path('school/update/<uuid:pk>', views.update_school, name='update-school'),
    path('school/delete/<uuid:pk>', views.delete_school, name='delete-school'),
    path('school/<uuid:pk>', views.get_one_school, name='detail-school'),

    path('classroom/create', views.create_classroom, name='add_class'),
    path('classroom/all', views.get_all_classroom, name='get_all_class'),
    path('classroom/list', views.get_classrooms, name='get_classes'),
    path('classroom/update/<uuid:pk>', views.update_classroom, name='update_class'),
    path('classroom/delete/<uuid:pk>', views.delete_classroom, name='delete_class'),
    path('classroom/<uuid:pk>', views.get_one_classroom, name='get_one_class'),

    path('student/create', views.add_student, name='add_student'),
    path('student/all', views.get_all_student, name='get_all_student'),
    path('student/list', views.get_students, name='get_students'),
    path('student/update/<uuid:pk>', views.update_student, name='update_student'),
    path('student/delete/<uuid:pk>', views.delete_student, name='delete_student'),
    path('student/<uuid:pk>', views.get_one_student, name='get_one_student'),
]
