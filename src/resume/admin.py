from django.contrib import admin
from .models import Profile, Education, Experience, Skills, Award, Project

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'github', 'wechat', 'introduction')
    search_fields = ('name', 'email', 'phone', 'address', 'github', 'wechat', 'introduction')
    list_filter = ('name', 'email', 'phone', 'address', 'github', 'wechat', 'introduction')

class EducationAdmin(admin.ModelAdmin):
    list_display = ('school', 'degree', 'major', 'rank', 'start_date', 'end_date', 'gpa', 'courses', 'description')
    search_fields = ('school', 'degree', 'major', 'rank', 'gpa', 'courses')
    list_filter = ('school', 'degree', 'major', 'rank', 'gpa', 'courses')

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'position', 'start_date', 'end_date', 'description')
    search_fields = ('company', 'position')
    list_filter = ('company', 'position')

class SkillsAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    search_fields = ('name', 'level')
    list_filter = ('name', 'level')

class AwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'date')
    search_fields = ('name', 'school')
    list_filter = ('name', 'school')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'start_date', 'end_date', 'description')
    search_fields = ('name', 'school')
    list_filter = ('name', 'school')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Skills, SkillsAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(Project, ProjectAdmin)

