from django.urls import path
from blog import views

#app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('post/<int:pk>/', views.PostDetailVies.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
    path('draft/', views.DraftListView.as_view(), name='post_draft_list'),
    path('post/<int:pk>/comment/', views.add_comment_to_post_view,
         name='add_comment_to_post'),
    path('post/<int:pk>/comment/approve/',
         views.approve_comment_view, name='approve_comment'),
    path('post/<int:pk>/comment/remove/',
         views.delete_comment_view, name='delete_comment'),
    path('post/<int:pk>/publish/',
         views.post_publish_view, name='post_publish'),

]
