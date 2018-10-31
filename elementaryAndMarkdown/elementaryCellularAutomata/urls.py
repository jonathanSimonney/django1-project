from django.urls import path

from . import views

app_name = 'elementaryCellularAutomata'
urlpatterns = [
    path('form/', views.WolframView.as_view(), name='wolfram_automata'),
    path('show/', views.wolfram_display, name='wolfram_automata_display'),
]
