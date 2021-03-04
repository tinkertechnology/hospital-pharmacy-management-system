from django.db import models

# Create your models here.

class Counter(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length = 200, unique=True) 
    created_at =   models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' %(self.name)   