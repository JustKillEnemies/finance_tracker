from django.urls import path, include, re_path, register_converter
from . import views

urlpatterns = [
    path('', views.TrackerHome.as_view(), name='home'),
    # path('operations/', views.operations, name='all_operations'),
    path('incomes/', views.incomes, name='incomes'),
    path('expenses/', views.expenses, name='expenses'),
    path('visual-report/', views.visual_report, name='visual_report'),
    path('feedback/', views.feedback, name='feedback'),
    path('create-operation/', views.CreateOperation.as_view(), name='create_operation'),
    path('create-category/', views.CreateCategory.as_view(), name='create_category')
]