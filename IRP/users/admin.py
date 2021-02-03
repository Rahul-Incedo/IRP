

from .forms import SignUpForm
from .models import CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
#from .models import User
# Register your models here.
#admin.site.register(User)

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    model = CustomUser
   # fields = ['email','employee_id', 'first_name','last_name']
    ordering = ('username','name')   # Here Username refers to Email
    
    # fields = ['username', 'password', 'name', 'employee_id']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('name',)}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    def create_user(username, self, password, **extra_fields):  # Here Username refers to Email
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user( username, password, **extra_fields)

    def create_superuser(username, self, password, **extra_fields):   # Here Username refers to Email
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)

    
admin.site.register(CustomUser, CustomUserAdmin)    

