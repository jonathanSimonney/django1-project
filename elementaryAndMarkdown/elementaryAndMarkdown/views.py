from django.shortcuts import render


def home_display(request):
    return render(request, 'index.html')
