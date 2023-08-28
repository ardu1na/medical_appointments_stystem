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
    
    phone = models.CharField(max_length=40, null=True, blank=True)
    whats_app = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
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
    
    direccion = models.CharField(max_length=400, null=True, blank=True)

    healt_insurance = models.ForeignKey(HealthInsurance, related_name="patients",verbose_name="obra social", on_delete=models.SET_NULL, null=True)
    
    insurance_data = models.CharField(verbose_name="N° de Afiliado", max_length=100, null=True, blank=True)
     
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
    
    def __str__ (self):
        return f'{self.last_name}, {self.name}'
    
class ClinicalHistory(BaseModel):
    patient = models.OneToOneField(Patient, verbose_name="paciente", related_name="history", on_delete=models.CASCADE)
    
    notes = models.TextField(null=True, verbose_name="Notas", blank=True)
    
    class Meta:
        verbose_name = "Historia Clínica"
        verbose_name_plural = "Historias Clínicas"
    
    
    def __str__ (self):
        return f'{self.patient} clinical history'



class Area(BaseModel):
    name = models.CharField(max_length=100, verbose_name="nombre")
    
    
    def __str__ (self):
        return self.name

class Doctor(BaseModel, PersonaBaseModel):
    area = models.ForeignKey(Area, verbose_name="área", related_name="doctors", on_delete=models.SET_NULL, null=True)
    class Meta:
        verbose_name_plural = "Doctores"

    def __str__ (self):
        return f'{self.last_name} ({self.area})'
    



class Recepcionist(BaseModel, PersonaBaseModel):
    user = models.OneToOneField(User, verbose_name="Nombre de Usuario", related_name="recepcionist_profile", on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Recepcionista"
        verbose_name_plural = "Recepcionistas"

    def __str__ (self):
        return f'{self.name} {self.last_name}'


class Appointment(BaseModel):
    patient = models.ForeignKey(Patient, related_name="appointments", verbose_name="paciente",on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name="appointments",verbose_name="doctor", on_delete=models.SET_NULL, null=True)
    
    receptionist = models.ForeignKey(
                            Recepcionist,
                            related_name="appointments",
                            verbose_name="recepcionista",
                            on_delete=models.SET_NULL, null=True)
    
    start_date = models.DateTimeField(verbose_name="Fecha de inicio",)
    end_date = models.DateTimeField(verbose_name="Fecha de culminación",)
    
    notes = models.TextField(null=True, verbose_name="Notas", blank=True)
    
    def __str__ (self):
        return f'{self.start_date} turno de {self.patient} con {self.doctor}'
    
    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"

