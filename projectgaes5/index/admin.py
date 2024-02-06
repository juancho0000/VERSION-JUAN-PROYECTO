from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Garantia, EstadosGarantia, ProductoServicio, Ocupacion, Trabajador, TipoDeServicio, Cita, Comentario, Contacto, Ventas
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class GarantiaResource(resources.ModelResource):
    class Meta:
        model = Garantia
        fields = ('id', 'fecha_vencimiento', 'codigo_garantia', 'detalles_garantia', 'detalles_vehiculo', 'estados', 'producto_servicio__nombre',)

@admin.register(Garantia)
class GarantiaAdmin(ImportExportModelAdmin):
    list_display = ('id', 'fecha_vencimiento', 'codigo_garantia', 'detalles_garantia', 'detalles_vehiculo', 'estados', 'nombre_producto_servicio',)
    search_fields = ('detalles_garantia', 'detalles_vehiculo',)
    list_filter = ('estados',)
    list_per_page = 10
    
    def nombre_producto_servicio(self, obj):
        return obj.producto_servicio.nombre if obj.producto_servicio else ''
    
    nombre_producto_servicio.short_description = 'Nombre del Producto o Servicio'

    def generar_informe_pdf(self, request, queryset):
        url = reverse('reporte_garantia_pdf')
        return format_html('<a class="button" href="{}" target="_blank">Generar Informe PDF</a>', url)

    generar_informe_pdf.short_description = 'Generar Informe PDF'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['mostrar_boton_pdf'] = True
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(EstadosGarantia)
class EstadosGarantiaAdmin(admin.ModelAdmin):
    list_display = ('estados',)
    


@admin.register(ProductoServicio)
class ProductoServicioAdmin(ImportExportModelAdmin):
    list_display = ('nombre', 'descripcion',)
    
class ProductoServicioResource(resources.ModelResource):
    class Meta:
        model = ProductoServicio
        
    

class OcupacionResource(resources.ModelResource):
    class Meta:
        model = Ocupacion

@admin.register(Ocupacion)
class OcupacionAdmin(ImportExportModelAdmin):
    resource_class = OcupacionResource
    list_display = ('nombre', 'descripcion',)
    search_fields = ('nombre', 'descripcion',)
    list_per_page = 10

class TrabajadorResource(resources.ModelResource):
    class Meta:
        model = Trabajador

@admin.register(Trabajador)
class TrabajadorAdmin(ImportExportModelAdmin):
    resource_class = TrabajadorResource
    list_display = ('nombre', 'apellido', 'email', 'ocupacion',)
    search_fields = ('nombre', 'apellido', 'email',)
    list_filter = ('ocupacion',)
    list_per_page = 10

class TipoDeServicioResource(resources.ModelResource):
    class Meta:
        model = TipoDeServicio

@admin.register(TipoDeServicio)
class TipoDeServicioAdmin(ImportExportModelAdmin):
    resource_class = TipoDeServicioResource
    list_display = ('nombre', 'descripcion',)
    search_fields = ('nombre', 'descripcion',)
    list_per_page = 10

class CitaResource(resources.ModelResource):
    class Meta:
        model = Cita

@admin.register(Cita)
class CitaAdmin(ImportExportModelAdmin):
    resource_class = CitaResource
    list_display = ('nombre', 'apellido', 'email', 'tipo_de_servicio', 'fecha', 'hora', 'trabajador',)
    search_fields = ('nombre', 'apellido', 'email',)
    list_filter = ('tipo_de_servicio', 'trabajador', 'fecha',)
    list_per_page = 10

class ComentarioResource(resources.ModelResource):
    class Meta:
        model = Comentario

@admin.register(Comentario)
class ComentarioAdmin(ImportExportModelAdmin):
    resource_class = ComentarioResource
    list_display = ('titulo', 'cita', 'descripcion',)
    search_fields = ('titulo', 'descripcion',)
    list_filter = ('cita',)
    list_per_page = 10

class ContactoResource(resources.ModelResource):
    class Meta:
        model = Contacto

@admin.register(Contacto)
class ContactoAdmin(ImportExportModelAdmin):
    resource_class = ContactoResource
    list_display = ('nombre', 'apellido', 'email', 'contacto',)
    search_fields = ('nombre', 'apellido', 'email',)
    list_filter = ('contacto',) 
    list_per_page = 10
    
    
class VentasResource(resources.ModelResource):
    class Meta:
        model = Contacto

@admin.register(Ventas)
class ContactoAdmin(ImportExportModelAdmin):
    resource_class = VentasResource
    list_display = ('detalles_venta','garantia_relacionada',)
    