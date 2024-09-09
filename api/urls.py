from django.urls import path

from .views.classroom import create_classroom, get_all_classroom, get_classrooms, update_classroom, delete_classroom, \
    get_one_classroom
from .views.school import add_school, get_all_school, get_schools, update_school, delete_school, get_one_school
from .views.student import add_student, get_all_student, get_students, update_student, delete_student, get_one_student

urlpatterns = [
    path('school/create', add_school, name='add-school'),
    path('school/all', get_all_school, name='view_school'),
    path('school/list', get_schools, name='view_schools'),
    path('school/update/<uuid:pk>', update_school, name='update-school'),
    path('school/delete/<uuid:pk>', delete_school, name='delete-school'),
    path('school/<uuid:pk>', get_one_school, name='detail-school'),

    path('classroom/create', create_classroom, name='add_class'),
    path('classroom/all', get_all_classroom, name='get_all_class'),
    path('classroom/list', get_classrooms, name='get_classes'),
    path('classroom/update/<uuid:pk>', update_classroom, name='update_class'),
    path('classroom/delete/<uuid:pk>', delete_classroom, name='delete_class'),
    path('classroom/<uuid:pk>', get_one_classroom, name='get_one_class'),

    path('student/create', add_student, name='add_student'),
    path('student/all', get_all_student, name='get_all_student'),
    path('student/list', get_students, name='get_students'),
    path('student/update/<uuid:pk>', update_student, name='update_student'),
    path('student/delete/<uuid:pk>', delete_student, name='delete_student'),
    path('student/<uuid:pk>', get_one_student, name='get_one_student'),
]
