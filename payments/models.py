from django.db import models

# Create your models here.
from django.db.models.fields import CharField

class PaymentStatus:
    SUCCESS = "Success"
    FAILURE = "Failure"
    PENDING = "Pending"

class Order(models.Model):
    name = CharField(max_length=254, blank=False, null=False)
    amount = models.FloatField(null=False, blank=False)
    status = CharField(default=PaymentStatus.PENDING,max_length=254,blank=False,null=False,)
    provider_order_id = models.CharField(max_length=40, null=False, blank=False)
    payment_id = models.CharField(max_length=36, null=False, blank=False)
    signature_id = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"
