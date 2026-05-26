from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobApplication
from .forms import JobApplicationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@login_required
def job_list(request):
    jobs = JobApplication.objects.filter(user=request.user)
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            messages.success(request, 'Application added!')
            return redirect('job_list')
    else:
        form = JobApplicationForm()
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
def job_edit(request, pk):
    job = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated!')
            return redirect('job_list')
    else:
        form = JobApplicationForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
def job_delete(request, pk):
    job = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Application deleted!')
        return redirect('job_list')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


@login_required
def dashboard(request):
    jobs = JobApplication.objects.filter(user=request.user)
    total = jobs.count()
    applied = jobs.filter(status='applied').count()
    interview = jobs.filter(status='interview').count()
    offer = jobs.filter(status='offer').count()
    rejected = jobs.filter(status='rejected').count()

    context = {
        'total': total,
        'applied': applied,
        'interview': interview,
        'offer': offer,
        'rejected': rejected,
        'recent_jobs': jobs.order_by('-date_applied')[:5],
    }
    return render(request, 'jobs/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})