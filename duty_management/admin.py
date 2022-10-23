from django.contrib import admin
from .models import Reservation, Register, ReservationJudge
# Register your models here.

admin.site.register(Reservation)
admin.site.register(Register)
admin.site.register(ReservationJudge)