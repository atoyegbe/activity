import uuid
from django.db import models
from workflow.models import Program, SiteProfile
from utils.models import CreatedModifiedDates, CreatedModifiedBy
from datetime import date
from dateutil.relativedelta import relativedelta


class Case(models.Model):
    """
    Keeps track of Individuals/Households and their usage/participation in services
    Spec: https://github.com/hikaya-io/activity/issues/410
    """
    # ! If Individuals already exist in the database, we change its ID
    # ! to UUID type, and hence can inherit from Case
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField(max_length=255)


class Household(Case):
    """
    Family, or group of people, living together
    Spec: https://github.com/hikaya-io/activity/issues/409
    """
    name = models.CharField(max_length=255)


class Individual(Case, CreatedModifiedDates, CreatedModifiedBy):
    """
    Individual, or person.
    Subject to future changes: https://github.com/hikaya-io/activity/issues/403
    Also, will inherit from Case (subject to research/discussion)
    """
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    sex = models.CharField(choices=SEX_CHOICES, max_length=1, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    household_id = models.ForeignKey(
        Household, null=True, blank=True, on_delete=models.SET_NULL)
    head_of_household = models.BooleanField(default=True)
    id_type = models.CharField(max_length=255, null=True, blank=True)
    id_number = models.CharField(max_length=255, null=True, blank=True)
    primary_number = models.IntegerField(null=True, blank=True)
    secondary_number = models.IntegerField(null=True, blank=True)
    signature = models.BooleanField(default=True)
    site = models.ForeignKey(
        SiteProfile, null=True, blank=True, on_delete=models.SET_NULL)
    photo = models.ImageField(upload_to=None, null=True, blank=True)
    description = models.TextField(max_length=550, null=True, blank=True)
    program = models.ForeignKey(
        Program, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def age(self):
        today = date.today()
        delta = relativedelta(today, self.date_of_birth)
        return delta.years

    class Meta:
        ordering = ('first_name',)

    def save(self, *args, **kwargs):
        super(Individual, self).save(*args, **kwargs)

    def __str__(self):
        if self.first_name is None:
            return "NULL"
        return self.first_name
