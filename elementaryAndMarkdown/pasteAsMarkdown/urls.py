from django.urls import path

from . import views

app_name = 'pasteAsMarkdown'
urlpatterns = [
    path('paste/', views.PastebinView.as_view(), name='markdown_paste'),
    path('show/<str:pastebin_path>', views.show_pastebin, name='show_result'),
    path('create', views.create_pastebin, name='create_pastebin'),
]
