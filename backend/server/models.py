from django.db import models

# Create your models here.
class Project(models.Model):
    repo_name = models.CharField(max_length=40)
    dao_address = models.CharField(max_length=40)


class ASC(models.Model):
    address = models.CharField(max_length=40)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
