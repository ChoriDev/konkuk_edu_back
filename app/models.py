from djongo import models

class Item(models.Model):
    no = models.CharField(max_length=2)
    name = models.CharField(max_length=20)
    student_id = models.CharField(max_length=9, default=None, null=True)
    student_name = models.CharField(max_length=20, default=None, null=True)
    phone_num = models.CharField(max_length=13, null=True, default=None)
    rental_date = models.DateTimeField(null=True, default=None)
    deadline_date = models.DateTimeField(null=True, default=None)
    state = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['no', 'name'], name='물품별 고유 번호 부여'),
        ]