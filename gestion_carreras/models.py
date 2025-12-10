# gestion_carreras/models.py
from django.db import models
from django.contrib.auth.models import User

class Facultad(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Facultades"


class Sede(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre


class Carrera(models.Model):
    GRADOS = [
        ('licenciatura', 'Licenciatura'),
        ('tecnico', 'Técnico Superior'),
    ]
    
    nombre = models.CharField(max_length=200)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    grado_academico = models.CharField(max_length=20, choices=GRADOS)
    
    def __str__(self):
        return self.nombre


class FaseCronograma(models.Model):
    codigo = models.CharField(max_length=10)
    nombre = models.TextField()
    medios_verificacion = models.TextField()
    orden = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        ordering = ['orden']


class EstadoCronograma(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
    ]
    
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    fase = models.ForeignKey(FaseCronograma, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_conclusion = models.DateField(null=True, blank=True)
    medios_verificacion = models.TextField(blank=True)
    observaciones = models.TextField(blank=True, default='')
    ultimo_editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.carrera.nombre} - {self.fase.codigo}"
    
    class Meta:
        unique_together = ['carrera', 'fase']


class ArchivoCronograma(models.Model):
    TIPOS_ARCHIVO = [
        ('acta', 'Acta'),
        ('informe', 'Informe'),
        ('documento', 'Documento'),
        ('presentacion', 'Presentación'),
        ('otro', 'Otro'),
    ]
    
    estado = models.ForeignKey(EstadoCronograma, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to='cronogramas/')
    nombre = models.CharField(max_length=255, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_ARCHIVO, default='documento')
    descripcion = models.TextField(blank=True)
    nombre_original = models.CharField(max_length=255)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    subido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.nombre or self.nombre_original
    
    class Meta:
        ordering = ['-fecha_subida']