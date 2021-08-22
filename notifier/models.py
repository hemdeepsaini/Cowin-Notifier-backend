from django.db import models

class Order(models.Model):
    class Meta:
        unique_together = (('pin', 'email'),)

    pin = models.CharField(max_length=6)
    email = models.CharField(max_length=30)
    age = models.IntegerField()
    count = models.IntegerField()
    # def __str__(self):
    #     return self.email

class Pin(models.Model):
    pin = models.CharField(max_length=6,unique=True)
    # Location = models.CharField(max_length=40)
    # def __str__(self):
    #     return self.pin

class Email(models.Model):
    pin = models.CharField(max_length=6)
    email = models.CharField(max_length=30)
