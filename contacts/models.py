from django.db import models


class Contact(models.Model):
    email = models.EmailField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)

    def __str__(self):
        return self.email
