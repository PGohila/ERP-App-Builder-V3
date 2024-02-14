from django.urls import path, include
from sub_part import views
from .views import *
urlpatterns = [
    path('get_projectid', views.get_projectid, name='get_projectid'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('success', views.success, name='success'),
    path('', views.create_project, name='create_project'),
    path('project_deletion', views.project_deletion, name='project_deletion'),
    path('create_dbform/', views.create_dbform, name='create_dbform'),
    path('edit_screen/<int:screen_id>/', views.edit_screen, name='edit_screen'),
    path('screen_elements/', views.screen_elements, name='screen_elements'),
    path('ajax_get_table_id/', views.ajax_get_table_id, name='ajax_get_table_id'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    
    path('upload_image/', views.upload_image, name='upload_image'),
    path('main_sub_menu_save/', views.main_sub_menu_save, name='main_sub_menu_save'),
    path('screen_element_with_orchestration/', views.screen_element_with_orchestration, name='screen_element_with_orchestration'),
    path('icon_master/', views.icon_master, name='icon_master'),
    path('select_screen/', views.select_screen, name='select_screen'),
    path('preview/<int:screen_id>/', views.preview_screen, name='preview_screen'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<str:project_name>/', views.download_project, name='project_download'),

    path('tables/', views.tables, name='tables'),
    path('user_type_master/', views.user_type_master, name='user_type_master'),
    path('screen_version_list/<int:screen_id>/', views.screen_version_list, name='screen-version-list'),
    path('screen_version_s1/<int:screen_id>/', views.screen_version_s1, name='screen_version_s1'),
    path('screen_version_s2/<int:screen_version_id>/', views.screen_version_s2, name='screen_version_s2'),
    path('screen_version_s3/<int:screen_version_id>/', views.screen_version_s3, name='screen_version_s3'),
    path('screen_preview/<int:screen_version_id>/', views.screen_preview, name='screen_preview'),
    # path('save_priority_order/', views.save_priority_order, name='save_priority_order'),
    path("project_setups/", SetupView.as_view(), name="project_setups"),
    path('demo_excel_export/', demo_excel_export, name='demo_excel_export'),
]
