from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=200)
    remarks = models.CharField(max_length=200)
    created_at =   models.DateTimeField(auto_now_add=True) # When it was create
    updated_at = models.DateTimeField(auto_now=True) # When i was update
    status = models.BooleanField(default=True)
    def __str__(self):
        return '%s' %(self.name)

class State(models.Model):
    name = models.CharField(max_length=200)
    created_at =  models.DateTimeField(auto_now_add=True) # When it was create
    updated_at = models.DateTimeField(auto_now=True) # When i was update
    status = models.BooleanField(default=True)
    def __str__(self):
        return '%s' %(self.name)

class District(models.Model):
    name = models.CharField(max_length=200)
    fk_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='state', null=True)
    created_at =   models.DateTimeField(auto_now_add=True) # When it was create
    updated_at = models.DateTimeField(auto_now=True) # When i was update
    status = models.BooleanField(default=True)
    def __str__(self):
        return '%s' %(self.name)

class LocalGov(models.Model):
    name = models.CharField(max_length=200)
    fk_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='district', null=True)
    localgov_type = models.CharField(max_length=200, null=True)
    created_at =   models.DateTimeField(auto_now_add=True) # When it was create
    updated_at = models.DateTimeField(auto_now=True) # When i was update
    status = models.BooleanField(default=True)
    def __str__(self):
        return '%s' %(self.name)