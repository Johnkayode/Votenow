from accounts.utils import decode_data
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UploadQrcodeForm, CreateContestForm, JoinContestForm
from .models import *

import cv2 as cv
import numpy as np
import os

def home(request):
    context = {}
    return render(request,'contests/index.html', context)

def verify(request):
    if request.method == 'POST':
        
        form = UploadQrcodeForm(request.POST, request.FILES)
        if form.is_valid():
            qrcode_str = request.FILES['qrcode'].read()
            npimg = np.fromstring(qrcode_str, np.uint8)
            im = cv.imdecode(npimg, cv.IMREAD_COLOR)
            det = cv.QRCodeDetector()
            retval, points, straight_qrcode = det.detectAndDecode(im)
            email = decode_data(retval)
            print(email)
            return redirect('contest:home')
    else:
        form = UploadQrcodeForm()
        context = {'form':form}
        return render(request, 'contests/verify.html', context)
        
@login_required
def contest(request):
    if request.method == 'POST':
        form= CreateContestForm(request.POST)
        if form.is_valid():
            contest = form.save(commit=False)
            contest.organizer = request.user
            contest.save()
            return redirect('account:dashboard', id=request.user.id)
    else:
        form = CreateContestForm()
        context = {'form':form}
        return render(request, 'contests/contest.html', context)

@login_required
def join_contest(request):
    if request.method == 'POST':
        form = JoinContestForm(request.POST)
        if form.is_valid():
            contest_code = form.cleaned_data['contest_code']
            manifesto = form.cleaned_data['manifesto']
            contest = Contest.objects.get(contest_code=contest_code)
            if contest:
                contestant = Contestant.objects.create(user=request.user,contest=contest, name=request.user.name, manifesto=manifesto)
                messages.success(request, 'Joined Contest sucessfully')
                return redirect('account:dashboard', id=request.user.id)
            else:
                context = {'form':form}
                messages.error(request, 'Contest does not exist')
                return render(request, 'contests/join.html', context)
    else:
        form = JoinContestForm()
        context = {'form':form}
        return render(request, 'contests/join.html', context)
