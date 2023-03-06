from django.db import models
import uuid

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)  
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True) 
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 
    # by default, every table will have an id field which will be auto incrementing. we make the field in order to override it.
    
    def __str__(self):
        return self.title

    # null=True means this field is not required and can be null. 
    # Blank=True means this can be let empty and will be ignored during validation.
    # auto_now_add=True: will give current date and timestamp whenever the record is created
    # unique=True means no other record must have the same id
    # editable=False: will prevent it from editing; will make it readonly