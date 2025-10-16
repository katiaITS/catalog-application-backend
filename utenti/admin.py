from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import ProfiloUtente

# Estendi l'admin di User per personalizzarlo se necessario
class CustomUserAdmin(BaseUserAdmin):
    # Usa i campi standard di Django
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_superuser','is_staff',  'is_active', 'groups')

# Deregistra l'admin di default e registra il nostro
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Registra ProfiloUtente
admin.site.register(ProfiloUtente)
