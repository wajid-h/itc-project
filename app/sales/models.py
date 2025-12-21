from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

PROFIT_MARGIN = 0.125  

class SaleGroup(models.Model):
    name =  models.CharField(max_length= 64)
    description = models.TextField(max_length = 256)
    creation_date = models.DateTimeField(auto_now_add= True)
    owner =  models.ForeignKey(User, related_name= "businesses"  , on_delete= models.CASCADE)   

    def __str__(self):
        return self.name

class Sale (models.Model):
    date = models.DateTimeField()
    sale = models.BigIntegerField(blank=True, default=0)
    expenses = models.BigIntegerField(blank=True, default=0)
    investment =  models.BigIntegerField(blank = True, default= 0)
    profit = models.BigIntegerField(blank=True, default=0)
    business = models.ForeignKey(SaleGroup, related_name= "sales", on_delete= models.CASCADE)

    def refresh_profit(self):
        try:
            computed = int(self.sale * PROFIT_MARGIN) - int(self.expenses)
        except Exception:
            computed = 0
        self.profit = computed
        self.save();
    
    def save(self, *args, **kwargs):    
        computed = int(self.sale * PROFIT_MARGIN) - int(self.expenses)      
        self.profit = computed
        return super().save(*args, **kwargs)

    def __str__(self):
        return str (self.date)  
    
