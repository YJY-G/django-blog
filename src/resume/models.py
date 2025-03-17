from django.db import models


# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='images/avatar/', null=True, blank=True)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    github = models.URLField(max_length=100)
    wechat = models.CharField(max_length=100)
    introduction = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Education(models.Model):
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    major = models.CharField(max_length=100,default='')
    rank = models.CharField(max_length=100,default='')
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    gpa = models.CharField(max_length=10,default='')
    courses = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def start_date_str(self):
        return self.start_date.strftime('%Y-%m')
    
    @property
    def end_date_str(self):
        return self.end_date.strftime('%Y-%m')
    
    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.school
    

class Experience(models.Model):
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company

    @property
    def start_date_str(self):
        return self.start_date.strftime('%Y-%m-%d')
    
    @property
    def end_date_str(self):
        return self.end_date.strftime('%Y-%m-%d')
    
    class Meta:
        ordering = ['-start_date']

class Skills(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Project(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(Education,on_delete=models.CASCADE,related_name='projects')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def start_date_str(self):
        return self.start_date.strftime('%Y-%m-%d')
    
    @property
    def end_date_str(self):
        return self.end_date.strftime('%Y-%m-%d')
    
    def __str__(self):
        return self.name
    
class Award(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(Education,on_delete=models.CASCADE,related_name='awards')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def date_str(self):
        return self.date.strftime('%Y-%m-%d')
    
    