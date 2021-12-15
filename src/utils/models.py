from django.db import models


# class AbstractAddressModel(models.Model):
#     country = models.ForeignKey(Country)
#     state = models.ForeignKey(State)
#     city = models.ForeignKey(City, null=True)
#     address = models.CharField(max_length=256, null=True, blank=True)
#     postal_code = models.CharField(max_length=64, verbose_name='zip/postal code')
#
#     class Meta:
#         abstract = True
from django.utils import timezone


class AbstractTimeStampModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractValidityModel(models.Model):
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def is_expired(self):
        if self.valid_to:
            return self.valid_to < timezone.now().today()
        return False
