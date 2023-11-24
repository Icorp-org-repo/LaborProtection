from django.contrib import admin
from .models import Company, Position, Employ, Admission, Protocol
# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    list_filter = ('created',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['created', 'title']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category')
    list_filter = ('category', 'company', )
    search_fields = ('title',)
    ordering = ('created',)


@admin.register(Employ)
class EmployAdmin(admin.ModelAdmin):
    list_display = ('number', 'second_name', 'name', 'surname', 'position','appointed', 'boss')
    list_filter = ('appointed', 'position', )
    search_fields = ('number','second_name', 'name', 'surname',)
    prepopulated_fields = {'slug': ('number',)}
    ordering = ('second_name', 'name', 'surname','created',)


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'knowledge', 'type')
    list_filter = ('knowledge', 'type')
    search_fields = ('title', 'body')
    ordering = ('title',)


@admin.register(Protocol)
class ProtocolAdmin(admin.ModelAdmin):
    list_display = ('status', 'employ', 'admission', 'start', 'end')
    list_filter = ('status', 'admission', 'start', 'end')
    search_fields = ('employ', 'admission', 'number')
