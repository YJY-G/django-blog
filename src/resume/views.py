from django.shortcuts import render
from .models import Profile, Education, Experience, Skills, Award, Project
# Create your views here.

def about(request):
    awards = Award.objects.all()
    projects = Project.objects.all()
    profile = Profile.objects.first()
    education = Education.objects.all()
    experience = Experience.objects.all()
    skills = Skills.objects.all()
    skills_num = len(skills)
    col_1 = skills[:skills_num//2]
    col_2 = skills[skills_num//2:]
    return render(request, 'about.html', {'profile': profile, 'education': education, 
                                          'experience': experience, 'skills': skills, "col_1": col_1, "col_2": col_2,
                                          'awards': awards, 'projects': projects})