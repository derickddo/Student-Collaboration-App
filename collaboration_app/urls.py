from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('create-group',views.create_group, name='create_group'),
    path('join-group',views.join_group, name='join_group'),
    path('join-public-group/<str:id>',views.join_public_group, name='join_public_group'),
    path('get-group/<str:id>',views.get_group, name='get_group'),
    path('update-group/<str:id>',views.update_group, name='update_group'),
    path('create-task/<str:id>',views.create_task, name='create_task'),
    path('add-member/<str:id>',views.add_member, name='add_member'),
    path('remove-member/<str:id>',views.remove_member, name='remove_member'),
    path('get-task/<str:id>',views.get_task, name='get_task'),
    path('delete-group/<str:id>',views.delete_group, name='delete_group'),
    path('update-task', views.update_task, name="update_task"),
    path('dashboard/private', views.private_dashboard, name="dashboard"),
    path('dashboard/public', views.public_dashboard, name="public_dashboard"),
    path('paraphrase', views.paraphrase_text, name="paraphrase_text"),
    path('accept_join_request/<str:id>', views.accept_join_request, name="accept_join_request"),
    path('delete-file/<str:id>', views.delete_file, name='delete_file'),
    path("profile/<str:id>", views.profile, name="profile")
]