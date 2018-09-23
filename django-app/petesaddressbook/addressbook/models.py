from django.db import models

class Contact(models.Model):
  first_names = models.CharField(max_length=100, null=True, blank=True)
  last_name = models.CharField(max_length=35)
  phone_number = models.CharField(max_length=15, null=True, blank=True)
  email_address = models.EmailField(null=True, blank=True)
  dob = models.DateField(null=True)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)

class Address(models.Model):
  ''' each address belongs to one contact (one-to-many relationship) '''
  contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='addresses')
  first_line = models.CharField(max_length=200, null=True, blank=True)
  second_line = models.CharField(max_length=200, null=True, blank=True)
  town = models.CharField(max_length=50, null=True, blank=True)
  county = models.CharField(max_length=50, null=True, blank=True)
  country = models.CharField(max_length=50, null=True, blank=True)
  postcode = models.CharField(max_length=10, null=True, blank=True)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
