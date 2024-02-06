from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random

# Función para generar código de garantía
def generate_codigo_garantia():
    return random.randint(1000, 9999)

# Validación de la fecha de vencimiento
def validate_fecha_vencimiento(value):
    today = timezone.now().date()
    six_months_later = today + timezone.timedelta(days=6 * 30)

    if value <= today:
        raise ValidationError(_('La fecha debe ser posterior a hoy.'))
    elif value > six_months_later:
        raise ValidationError(_('La fecha no puede ser posterior a 6 meses a partir de hoy.'))

class EstadosGarantia(models.Model):
    estados = models.CharField(max_length=20)

    def __str__(self):
        return self.estados

    class Meta:
        verbose_name = "Estado de Garantía"
        verbose_name_plural = "Estados de Garantía"
        db_table = "EstadosGarantia"
        ordering = ['id']

class ProductoServicio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Producto o Servicio"
        verbose_name_plural = "Productos y Servicios"
        db_table = "ProductoServicio"
        ordering = ['id']

class Garantia(models.Model):
    fecha_vencimiento = models.DateField(validators=[validate_fecha_vencimiento])
    codigo_garantia = models.PositiveIntegerField(unique=True, default=generate_codigo_garantia)
    detalles_garantia = models.CharField(max_length=100)
    detalles_vehiculo = models.CharField(max_length=80)
    estados = models.ForeignKey(EstadosGarantia, on_delete=models.CASCADE)
    
    # Relación con ProductoServicio
    producto_servicio = models.ForeignKey(ProductoServicio, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"ID: {self.id} - Estado: {self.estados.estados}"

    class Meta:
        verbose_name = "Garantía"
        verbose_name_plural = "Garantías"
        db_table = "Garantia"
        ordering = ['id']

# CITAS

class Ocupacion(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Ocupación'
        verbose_name_plural = 'Ocupaciones'
        db_table = 'ocupacion'
        ordering = ['id']

class Trabajador(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()
    ocupacion = models.ForeignKey(Ocupacion, on_delete=models.CASCADE)
  
    def __str__(self):
        return "%s %s" % (self.nombre, self.apellido)

    class Meta:
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajadores'
        db_table = 'trabajadores'
        ordering = ['id']
        
class TipoDeServicio(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tipo de Servicio'
        verbose_name_plural = 'Tipos de Servicios'
        db_table = 'tipo_de_servicio'
        ordering = ['id']
        
class Cita(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()
    tipo_de_servicio = models.ForeignKey(TipoDeServicio, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.tipo_de_servicio.nombre}"

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        db_table = 'cita'
        ordering = ['id']

class Comentario(models.Model):
    titulo = models.CharField(max_length=30)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        db_table = 'comentario'
        ordering = ['id']

class Contacto(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()
    contacto = models.IntegerField()

    def __str__(self):
        return "%s %s" % (self.nombre, self.apellido)

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        db_table = 'contactos'
        ordering = ['id']

# VENTAS

class Ventas(models.Model):
    fecha_venta = models.DateField(default=timezone.now)
    monto_venta = models.DecimalField(max_digits=10, decimal_places=2)
    detalles_venta = models.TextField()
    garantia_relacionada = models.OneToOneField(Garantia, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"ID: {self.id} - Fecha de Venta: {self.fecha_venta} - Monto: {self.monto_venta}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        db_table = "Ventas"
        ordering = ['id']
