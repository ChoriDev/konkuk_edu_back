from djongo import models

class Item(models.Model):
    no = models.CharField(max_length=2)
    name = models.CharField(max_length=20)
    student_id = models.CharField(max_length=9, null=True)
    student_name = models.CharField(max_length=20, null=True)
    rental_date = models.DateTimeField(null=True)
    deadline_date = models.DateTimeField(null=True)
    state = models.BooleanField(default=True)