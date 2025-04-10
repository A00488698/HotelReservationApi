import random
import string
from django.db import models
from django.utils import timezone
from django.db import connection

def generate_confirmation_number():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    digits = ''.join(random.choices(string.digits, k=5))
    return letters + digits

def confirmation_exists(confirmation):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1 FROM reservations_reservation WHERE confirmation_number = %s LIMIT 1", [confirmation])
        return cursor.fetchone() is not None
class Hotel(models.Model):
    name = models.CharField(max_length=100, verbose_name="酒店名称", default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格", default=0.00)
    available = models.BooleanField(default=True, verbose_name="可预订")

    def __str__(self):
        return self.name

class Reservation(models.Model):
    hotel_name = models.CharField(max_length=100, verbose_name="关联酒店", default="")
    check_in = models.DateField(verbose_name="入住日期", default=timezone.now)
    check_out = models.DateField(verbose_name="退房日期", default=timezone.now)
    customer_name = models.CharField(max_length=100, verbose_name="预定者姓名", default="")
    confirmation_number = models.CharField(max_length=20, unique=True, verbose_name="确认号", default="")
    guests_list = models.JSONField(default=list, verbose_name="客人列表")  # 存储客人列表的JSON
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总价", default=0.00)

    def __str__(self):
        return f"{self.customer_name} - {self.hotel_name}"

    def save(self, *args, **kwargs):
        if not self.confirmation_number:
            confirmation = generate_confirmation_number()
            # 使用 confirmation_exists 函数查询数据库确保生成的确认号唯一
            while confirmation_exists(confirmation):
                confirmation = generate_confirmation_number()
            self.confirmation_number = confirmation
        super().save(*args, **kwargs)