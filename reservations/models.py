from datetime import date
today = date.today()

from django.db import models
from django.contrib.auth.models import User


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
     
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
    
    def __str__ (self):
        return f'{self.last_name}, {self.name}'
    

class Area(BaseModel):
    name = models.CharField(max_length=100, verbose_name="nombre")
    
    
    def __str__ (self):
        return self.name

class Doctor(BaseModel, PersonaBaseModel):
    area = models.ForeignKey(Area, verbose_name="área", related_name="doctors", on_delete=models.SET_NULL, null=True)
    class Meta:
        verbose_name_plural = "Médicos"
        verbose_name = "Médico"

    def __str__ (self):
        inicial = self.name[-1].upper()
        return f'{self.last_name} {inicial}. ({self.area.name})'
    



class Recepcionist(BaseModel, PersonaBaseModel):
    user = models.OneToOneField(
                    User,
                    verbose_name="Nombre de Usuario",
                    related_name="recepcionist",
                    on_delete=models.CASCADE, blank=True, null=True)
    
    
    phone = models.CharField(max_length=40, null=True, blank=True)
    whats_app = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField()
    
    class Meta:
        verbose_name = "Recepcionista"
        verbose_name_plural = "Recepcionistas"

    def __str__ (self):
        return f'{self.name} {self.last_name}'
    
           
    def save(self, *args, **kwargs):
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
            self.user.save()
        super().save(*args, **kwargs)



class Appointment(BaseModel):
    patient = models.ForeignKey(Patient, related_name="appointments", verbose_name="paciente",on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name="appointments",verbose_name="doctor", on_delete=models.SET_NULL, null=True)
    
    recepcionist = models.ForeignKey(
                            Recepcionist,
                            related_name="appointments",
                            verbose_name="recepcionista",
                            on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    
    start_date = models.DateTimeField(verbose_name="Fecha de inicio",)
    end_date = models.DateTimeField(verbose_name="Fecha de culminación",)
    
    notes = models.TextField(null=True, verbose_name="Notas", blank=True)
    
    @property
    def area(self):
        return self.doctor.area
    
    @property
    def start(self):
        date = self.start_date.strftime('%H:%M %d/%m')
        return date
    
    
    @property
    def end(self):
        date = self.end_date.strftime('%H:%M %d/%m')
        return date
    
    
    
    def __str__ (self):
        date = self.start_date.strftime('%H:%M %d/%m')

        return f'{date} | {self.doctor}'
    
    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        
        