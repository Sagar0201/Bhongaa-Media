from django.db import models

# Create your models here.


class Posts(models.Model):
    file = models.FileField(upload_to="static/images", null=True)
    file_type = models.CharField(max_length=10)
    Title = models.CharField(max_length=100)
    Category = models.CharField(max_length=100,default='images')
    Description = models.TextField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Title

    class Meta:
        ordering = ('timestamp',)


class ContactInfo(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.CharField(max_length=50)
    message_subject = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
