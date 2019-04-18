from django.db import models

# Create your models here.

class Questions(models.Model):
    question = models.CharField(max_length=50)
    def __str__(self):
        return self.question

class Choices(models.Model):
    choice = models.CharField(max_length=20)
    num = models.IntegerField(max_length=10)
    cquesid = models.ForeignKey('Questions', on_delete=models.CASCADE)
    def __str__(self):
        return self.choice