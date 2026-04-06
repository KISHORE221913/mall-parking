from django.db import models # import django db models module
import random # import py random module but here it import random num for tkt id

class Vehicle(models.Model): # defines a model table name vechicle , modeles.model is base class for all danjo models
    vehicle_number = models.CharField(max_length=20) # stores vech num, charfield means textfield ,max leng of the text is 20char
    vehicle_type = models.CharField(max_length=10) # same like vech type text size 10char bike or car
    is_vip = models.BooleanField(default=False) # for vip access yes or no ...default no stors as normal vech
    ticket_id = models.IntegerField(unique=True) # tkt num stores..unique id no 2 vechh has same num
    slot = models.CharField(max_length=10, null=True, blank=True) #parking slot num , null true = db store null if not it throws error, blank true without this form will show error
    floor = models.CharField(max_length=10, null=True, blank=True) # parking floor like 1st or 2nd
    entry_time = models.DateTimeField(auto_now_add=True) # stores entry time automatic
    exit_time = models.DateTimeField(null=True, blank=True) # stores exit time ..have to enter manually
    total_hours = models.IntegerField(null=True, blank=True) #stores total parked time in hrs
    bill = models.IntegerField(null=True, blank=True) # stores parking fee
    email = models.EmailField(null=True, blank=True) # stores user email...validate email formte automatic
    
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = random.randint(1000, 9999)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.vehicle_number

# #You are overriding Django’s default save()
# self → current object (vehicle)
# *args, **kwargs → extra arguments (passed to original save)
#Checks if ticket_id is empty
#Runs only when creating a new record
#

#This model stores vehicle parking details
# Includes:
# Vehicle info
# Entry/exit time
# Parking slot
# Billing info
# Automatically generates a ticket ID 
