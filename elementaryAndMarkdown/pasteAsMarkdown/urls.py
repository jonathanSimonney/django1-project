from django.urls import path

from . import views

app_name = 'pasteAsMarkdown'
urlpatterns = [
    path('paste/', views.PastebinView.as_view(), name='markdown_paste'),
    # path('show/<string:markdown_path>', ..., name='show_result'),
    path('create', views.create_pastebin, name='create_pastebin'),
]
