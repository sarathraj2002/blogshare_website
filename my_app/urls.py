from django.urls import path
from . import views


urlpatterns=[
    path('', views.home_view, name='home'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('create/',views.create_post,name='create_post'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('password_reset_form/', views.custom_password_reset_view, name='password_reset_form'),
    path('password_complete/', views.password_reset_done, name='password_complete'),
    # path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('add-comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),

]