from django.contrib import admin
from .models import Contract,Client,Payment
# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'email', 'user', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'passport_data')

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('number', 'client', 'house', 'total_amount', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'start_date')
    search_fields = ('number', 'client__full_name', 'client__phone')
    inlines = [PaymentInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('contract__number', 'contract__client__full_name')
    