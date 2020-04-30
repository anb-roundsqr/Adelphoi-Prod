# from django.contrib import admin
# from  import views

from django.urls import path
from . import views, update_api , pdf_generation
# from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Adelphoi API documnetation')
urlpatterns = [
    path('documentation/', schema_view),  # swagger_documentation
    # path('index/<pk>/',views.index),
    path('index/<pk>/',pdf_generation.index),
    path('list_view/', views.AdelphoiList.as_view()),
    path('result/<pk>/', views.Adelphoi_placement.as_view()),
    path('location/<pk>/', views.Adelphoi_location.as_view()),  # w
    path('update_list/<pk>/', views.AdelphoiResult.as_view()),  # w
    path('program_complete/<pk>/',
         views.ProgramCompletionLevel.as_view()),  # w
    path('search/', views.ClientList.as_view()),
    path('save', views.saveData),
    path('available_programs', views.AvailablePrograms.as_view()),
    path('refer/<pk>/', views.Adelphoi_referredprogram.as_view()),

    path('program_save', views.programSave),  # add new program
    path('program_list', views.Program_list.as_view()),  # list of programs
    path('programs/<pk>/', views.ProgramModify.as_view()),  # modify program
    path('location_save', views.locationSave),  # add new locations
    path('location_list',
         views.Location_list.as_view()),  # list of locations
    path('locations/<pk>/',
         views.LocationModify.as_view()),  # Modify locations
    path('program_pcr/<pk>/', views.RecommndedProgramPCR.as_view()),
    # path('render_pdf/<pk>/',views.render_pdf),
    path('dataSave', views.dataSave),# not using
    path('program/<pk>/', views.Adelphoi_program.as_view()),

    path('referral_list', views.Refferal_list.as_view()),
    path('referral_save', views.referralSave),
    path('referral_modify/<pk>/', views.referralModify.as_view()),

    path('latest_update/<pk>/', update_api.update_logic)

    # path('program/<pk>/',views.Adelphoi_program.as_view()), #w
    # path('admins/', views.AdminUpdate.as_view()), #<int:gender>
    # path('test',views.admin_submission),
    # path('locations/<pk>',views.Location_Mapping.as_view()),

]
