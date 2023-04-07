from django.db import models
from user.models import UserModel
import datetime
# Create your models here.

class Product(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )
    size = models.CharField(choices=sizes, max_length=1)
    inbound_count = models.IntegerField(default=0)
    unbound_count = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    inbound_date = models.DateTimeField(blank=True, null=True )
    unbound_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.code
    
    def save(self, *args, **kwargs):
        if not self.id: # 생성시 id가 없음 -> 생성동작
            super().save(*args, **kwargs)# 부모클래스의 save() 호출
        else:
        # do update
            previous_product = Product.objects.get(id=self.id)
            if self.stock != previous_product.stock:
                # count가 변경되었으므로 업데이트 수행
                diff = self.stock - previous_product.stock # 변경된 수량
                self.inbound_date = datetime.datetime.now() if diff > 0 else self.inbound_date
                self.unbound_date = datetime.datetime.now() if diff < 0 else self.unbound_date 
            super().save(*args, **kwargs)# 부모클래스의 save() 호출