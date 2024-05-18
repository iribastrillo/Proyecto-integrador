from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AbstractProfile (models.Model):
    birthdate = models.DateField()
    user = models.OneToOneField (User, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
        
class PrincipalProfile (AbstractProfile):
    ...