from django.shortcuts import render



def home(request):
    context = {}
    return render(request,'contests/index.html', context)
