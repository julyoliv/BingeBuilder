from django.db import models
from django.contrib.auth.models import User

class Event (models.Model):
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    finish_date = models.DateField()
    logo = models.ImageField(upload_to='logos')
    users = models.ManyToManyField(User, related_name="part_event", null=True, blank=True)

    #color pallete
    main_color = models.CharField(max_length=7)
    secondary_color = models.CharField(max_length=7)
    bg_color = models.CharField(max_length=7)

    def __str__(self) -> str:
        return self.name

class Certificate(models.Model):
    certificate = models.ImageField(upload_to="certificates")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
