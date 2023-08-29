from datetime import date
today = date.today()

from django.db import models
from django.contrib.auth.models import User, Group


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        abstract = True
        
class PersonaBaseModel(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    last_name = models.CharField(max_length=150,verbose_name="Apellido")
    phone = models.CharField(max_length=40, null=True, blank=True, verbose_name="teléfono")
    
    class Meta:
        abstract = True
        
     
class HealthInsurance(BaseModel):
    name = models.CharField(max_length=100, verbose_name="nombre")

    class Meta:
        verbose_name = "Obra Social"
        verbose_name_plural = "Obras Sociales"
    
    def __str__ (self):
        return self.name
    
        
class Patient(BaseModel, PersonaBaseModel):
    identification = models.PositiveIntegerField(verbose_name="DNI")

    GENDER_CHOICES = [
        ("M", "Masculino"),
        ("F", "Femenino"),
        ]
    gender = models.CharField(choices=GENDER_CHOICES, null=True, default=None, verbose_name="sexo", max_length=20)
    dob = models.DateField(verbose_name="Fecha de nacimiento")
    
    @property
    def edad(self):
        current_age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return current_age
    
    direccion = models.CharField(max_length=400, null=True, blank=True)

    
    
    whats_app = models.CharField(max_length=40, null=True, blank=True, verbose_name="Whats App")
    email = models.EmailField(null=True, blank=True)
    
    healt_insurance = models.ForeignKey(HealthInsurance, related_name="patients",verbose_name="obra social", on_delete=models.SET_NULL, null=True)
    
    insurance_data = models.CharField(verbose_name="N° de Afiliado", max_length=100, null=True, blank=True)   
    
    notes = models.TextField(null=True, verbose_name="Notas", blank=True)
    
    referent_1 = models.ForeignKey('Patient', related_name="patients", verbose_name="Referente",on_delete=models.SET_NULL, null=True, blank=True)
    
    referent_2 = models.ForeignKey('Patient', related_name="patients2", verbose_name="Referente",on_delete=models.SET_NULL, null=True, blank=True) 
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        
    def save(self, *args, **kwargs):
        n = self.name
        n = n.capitalize()
        self.name = n
        
        ln = self.last_name
        ln = ln.capitalize()
        self.last_name = ln
        
        super().save(*args, **kwargs)
    
    def __str__ (self):
        return f'{self.last_name}, {self.name}'
    

class Area(BaseModel):
    name = models.CharField(max_length=100, verbose_name="nombre")
    
     
    def save(self, *args, **kwargs):
        n = self.name
        n = n.upper()
        self.name = n
        
        
        super().save(*args, **kwargs)
        
    def __str__ (self):
        return self.name

class Doctor(BaseModel, PersonaBaseModel):
    area = models.ForeignKey(Area, verbose_name="área", related_name="doctors", on_delete=models.SET_NULL, null=True)
    
    notes = models.TextField(null=True, verbose_name="", blank=True)
    
    class Meta:
        verbose_name_plural = "Profesionales"
        verbose_name = "Profesional"
    
     
    def save(self, *args, **kwargs):
        n = self.name
        n = n.capitalize()
        self.name = n
        
        ln = self.last_name
        ln = ln.capitalize()
        self.last_name = ln
        
        super().save(*args, **kwargs)
        
        
    def __str__ (self):
        inicial = self.name[-1].upper()
        return f'{self.last_name} {inicial}. ({self.area.name})'
    
class DoctorAgenda(BaseModel):
    doctor = models.ForeignKey(
        Doctor, related_name="agendas",verbose_name="profesional", on_delete=models.SET_NULL, null=True)
    
    office = models.ForeignKey(
        'Office', related_name="agendas",verbose_name="consultorio", on_delete=models.SET_NULL, null=True)
    
    date = models.DateField(
        verbose_name="Día",)
    
    notes = models.TextField(null=True, verbose_name="Notas", blank=True)
    
    class Meta:
        verbose_name_plural = "Agendas"
        verbose_name = "Agenda"
    
    
    def __str__ (self):
        inicial = self.doctor.name[-1].upper()
        f_date = self.date.strftime('%d/%m')
        return f'{f_date} {self.doctor.last_name} {inicial}. ({self.doctor.area.name})'

class Recepcionist(BaseModel, PersonaBaseModel):
    user = models.OneToOneField(
                    User,
                    verbose_name="Nombre de Usuario",
                    related_name="recepcionist",
                    on_delete=models.CASCADE, blank=True, null=True, editable=False)
    
     
    def save(self, *args, **kwargs):
        n = self.name
        n = n.capitalize()
        self.name = n
        
        ln = self.last_name
        ln = ln.capitalize()
        self.last_name = ln
        
        super().save(*args, **kwargs)
    phone = models.CharField(max_length=40, null=True, blank=True)
    whats_app = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField()
    
    class Meta:
        verbose_name = "Recepcionista"
        verbose_name_plural = "Recepcionistas"

    def __str__ (self):
        return f'{self.name} {self.last_name}'
    
           
    def save(self, *args, **kwargs):
         
        n = self.name
        n = n.capitalize()
        self.name = n
        
        ln = self.last_name
        ln = ln.capitalize()
        self.last_name = ln
        
        
        if not self.user:
            name = self.name.lower().replace(' ', '_')
            last_name = self.last_name.lower().replace(' ', '_')
            
            self.user = User.objects.create_user(
                    username = f'{name}_{last_name}',
                    email = self.email,
                    password = "contraseña123", # pedirle al usuario que actualice su contraseña al registrase
                    first_name=self.name,
                    last_name=self.last_name,
                    is_active = True,
                    is_staff = True,

                    
                                    )
            receptionist_group = Group.objects.filter(name="recepcionistas").first()
            if receptionist_group == None:
                receptionist_group = Group.objects.create(name="recepcionistas")
            self.user.groups.add(receptionist_group) 
            self.user.save()
        super().save(*args, **kwargs)

class Office(BaseModel):
    number = models.PositiveSmallIntegerField(verbose_name="número")
    def __str__ (self):
        return str(self.number)
    
    class Meta:
        verbose_name = "Consultorio"
        verbose_name_plural = "Consultorios"

class Appointment(BaseModel):
    patient = models.ForeignKey(
        Patient, related_name="appointments", verbose_name="paciente",on_delete=models.CASCADE)
    
    ship = models.ForeignKey(
        DoctorAgenda, related_name="appointments",verbose_name="turno", on_delete=models.SET_NULL, null=True)
    
    recepcionist = models.ForeignKey(
                            Recepcionist,
                            related_name="appointments",
                            verbose_name="recepcionista",
                            on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    
    start = models.TimeField(
        verbose_name="Hora", null=True)
    arrival_date = models.TimeField(
        verbose_name="Llegada", blank=True, null=True)
    
    notes = models.TextField(null=True, verbose_name="Notas", blank=True)
    
    @property
    def area(self):
        return self.ship.doctor.area
    
    @property
    def office(self):
        return self.ship.office
    
    @property
    def doctor(self):
        d = f'{self.ship.doctor.last_name} {self.ship.doctor.name[-1].upper()}'
        return d
    
    
    
    
    
    
    def __str__ (self):
        date = self.start.strftime('%H:%M')

        return f'{date} | {self.ship.doctor}'
    
    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        
        
        
        """
        

class time_slots(models.Model):
    doctor_id=models.CharField(max_length=100)
    from_time=models.CharField(max_length=10)
    to_time=models.CharField(max_length=10)

    class Meta:
        db_table='time_slots'
        
        """