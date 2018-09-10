from django.contrib import admin

# Register your models here.
from .models import *

class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 3
 

class OrderAdmin(admin.ModelAdmin):
    '''
        Admin View for Order
    '''
    # list_display = ('',)
    list_filter = ('approved',)
    inlines = [
        OrderDetailInline,
    ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)

admin.site.register(Order, OrderAdmin)

admin.site.register(Medicine)
# admin.site.register(Order)	