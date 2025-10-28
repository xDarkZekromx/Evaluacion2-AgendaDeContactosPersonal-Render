from django.contrib import admin
from django.db.models import Q        
from .models import Contacto


# ---- Filtros personalizados ----

class PhoneTypeFilter(admin.SimpleListFilter):
    title = "tipo de teléfono"
    parameter_name = "tipo_tel"

    def lookups(self, request, model_admin):
        return [
            ("casa", "Casa (empieza con 2)"),
            ("movil", "Móvil (empieza con 9)"),
        ]

    def queryset(self, request, queryset):
        v = self.value()
        if v == "casa":
            return queryset.filter(telefono__startswith="2")
        if v == "movil":
            return queryset.filter(telefono__startswith="9")
        return queryset


class EmailDomainFilter(admin.SimpleListFilter):
    title = "dominio de correo"
    parameter_name = "dominio"

    def lookups(self, request, model_admin):
        # Puedes dejar estáticos los más comunes:
        comunes = [
            ("gmail.com", "gmail.com"),
            ("outlook", "outlook/hotmail/live"),
            ("yahoo.com", "yahoo.com"),
            ("otros", "Otros dominios"),
        ]
        return comunes

    def queryset(self, request, queryset):
        v = self.value()
        if v == "gmail.com":
            return queryset.filter(correo__iendswith="@gmail.com")
        if v == "yahoo.com":
            return queryset.filter(correo__iendswith="@yahoo.com")
        if v == "outlook":
            return queryset.filter(
                Q(correo__iendswith="@outlook.com")
                | Q(correo__iendswith="@hotmail.com")
                | Q(correo__iendswith="@live.com")
            )
        if v == "otros":
            return queryset.exclude(
                Q(correo__iendswith="@gmail.com")
                | Q(correo__iendswith="@yahoo.com")
                | Q(correo__iendswith="@outlook.com")
                | Q(correo__iendswith="@hotmail.com")
                | Q(correo__iendswith="@live.com")
            )
        return queryset


class NombreInicialFilter(admin.SimpleListFilter):
    title = "inicial del nombre"
    parameter_name = "ini"

    def lookups(self, request, model_admin):
        # Letras A–Z
        return [(chr(c), chr(c)) for c in range(ord("A"), ord("Z") + 1)]

    def queryset(self, request, queryset):
        v = self.value()
        if v:
            return queryset.filter(nombre__istartswith=v)
        return queryset


# ---- Admin del modelo ----

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "telefono", "correo", "direccion")
    search_fields = ("nombre", "telefono", "correo", "direccion")
    list_filter = (PhoneTypeFilter, EmailDomainFilter, NombreInicialFilter)
    ordering = ("nombre",)
    list_per_page = 25

    # acción para exportar a CSV desde el admin
    actions = ["exportar_csv"]

    def exportar_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        resp = HttpResponse(content_type="text/csv")
        resp["Content-Disposition"] = 'attachment; filename="contactos.csv"'
        writer = csv.writer(resp)
        writer.writerow(["id", "nombre", "telefono", "correo", "direccion"])
        for c in queryset:
            writer.writerow([c.id, c.nombre, c.telefono, c.correo, c.direccion])
        return resp

    exportar_csv.short_description = "Exportar contactos seleccionados a CSV"
