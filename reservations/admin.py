from django.contrib import admin
from reservations.models import Patient, Doctor, \
    Recepcionist, HealthInsurance, Area, \
    ClinicalHistory, Appointment
    
admin.site.register(Patient)
admin.site.register(Recepcionist)
admin.site.register(HealthInsurance)
admin.site.register(Area)
admin.site.register(ClinicalHistory)
admin.site.register(Appointment)



class AppointmentDoctor(admin.StackedInline):
    model = Appointment
    extra = 0

class DoctorAdmin(admin.ModelAdmin):
    inlines = [AppointmentDoctor,]
admin.site.register(Doctor, DoctorAdmin)
