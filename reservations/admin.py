from django.contrib import admin

from reservations.models import Patient, Doctor, \
    Recepcionist, HealthInsurance, Area, \
    Appointment




admin.site.site_header = 'Turnos Médicos'
admin.site.index_title = 'Administración'
admin.site.site_title = 'Administración'


    
admin.site.register(Recepcionist)


class DoctorInline(admin.StackedInline):
    model = Doctor
    extra = 0
    show_change_link = True
    
class AreaAdmin(admin.ModelAdmin):
    inlines = [DoctorInline,]
    list_display = ['name', 'medicos']
    search_fields = ['name']
   
    @admin.display(description='Staff')
    def medicos(self, obj, *args):
        s = ""
        medicos = obj.doctors.all()
        if medicos:
            for index, medico in enumerate(medicos):
                s += medico.name + ' ' + medico.last_name
                if index < len(medicos) - 1:
                    s += ', '
        return s

                
admin.site.register(Area, AreaAdmin)
    

class PatientInline(admin.StackedInline):
    model = Patient
    extra = 0
    show_change_link = True

class HealthInsuranceAdmin(admin.ModelAdmin):
    inlines = [PatientInline,]
admin.site.register(HealthInsurance, HealthInsuranceAdmin) 
    
class AppointmentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.recepcionist:
            obj.recepcionist = request.user.recepcionist
        obj.save()
    list_display = ['start', 'end', 'patient', 'doctor', 'area', 'recepcionist']
    list_display_links = ['start' , 'end', 'patient']
    search_fields = ['patient__name','patient__last_name', 'doctor__last_name', 'doctor__name', 'doctor__area__name']
    date_hierarchy = 'start_date'

admin.site.register(Appointment, AppointmentAdmin)


class AppointmentInline(admin.StackedInline):
    model = Appointment
    extra = 0
    show_change_link = True

class DoctorAdmin(admin.ModelAdmin):
    inlines = [AppointmentInline,]
    list_display = ['id', 'name', 'last_name', 'area']
    search_fields = ['name', 'last_name', 'area']
    list_filter = ['area']
    list_display_links = ['id' , 'name', 'last_name', 'area']
admin.site.register(Doctor, DoctorAdmin)



class PatientAdmin(admin.ModelAdmin):
    inlines = [AppointmentInline,]
    list_display = ['id', 'name', 'last_name', 'identification', 'gender', 'edad', 'healt_insurance', 'insurance_data']
    search_fields = ['name', 'last_name']
    list_filter = ['healt_insurance','gender']
    list_display_links = ['id' , 'name', 'last_name']
    
    
    fieldsets = (
        ('Datos Personales', {
            'fields': ('name', 'last_name', 'identification', 'dob', 'gender')
        }),
        ('Contacto', {
            'fields':  ('direccion', 'phone', 'whats_app', 'email')
        }),
        ('Obra social', {
            'fields':  ('healt_insurance', 'insurance_data',)
        }),
        (None, {
            'fields': ( 'notes',)
        })
    )
admin.site.register(Patient, PatientAdmin)
