from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title=models.CharField(max_length=50)
    description=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    price=models.IntegerField()

    def __str__(self):
        return str(self.author)
    


        

# Create your models here.
