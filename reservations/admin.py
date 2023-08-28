from django.contrib import admin

from reservations.models import Patient, Doctor, \
    Recepcionist, HealthInsurance, Area, \
    ClinicalHistory, Appointment
    
admin.site.register(Recepcionist)
admin.site.register(HealthInsurance)
admin.site.register(Area)
admin.site.register(ClinicalHistory)

"""
    TODO:
    # AUTO ASIGN GROUP "RECEPCIONISTAS INTO USER WHEN A RECEPTIONIST IS CREATED
    # THE RECEPTIONIST CAN OR CANT SEE ANOHER RECEPTIONIST SHIPS?
    #     
"""

class AppointmentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.recepcionist:
            obj.recepcionist = request.user.recepcionist
        obj.save()
admin.site.register(Appointment, AppointmentAdmin)





class AppointmentInline(admin.StackedInline):
    model = Appointment
    extra = 0

class DoctorAdmin(admin.ModelAdmin):
    inlines = [AppointmentInline,]
admin.site.register(Doctor, DoctorAdmin)



class PatientAdmin(admin.ModelAdmin):
    inlines = [AppointmentInline,]
admin.site.register(Patient, PatientAdmin)
