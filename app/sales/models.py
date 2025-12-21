from django.db import models

PROFIT_MARGIN = 0.125;

# Create your models here.
class Sale (models.Model):
    date = models.DateTimeField(auto_now_add=True)
    sale = models.BigIntegerField(blank=True, default=0)
    expenses = models.BigIntegerField(blank=True, default=0)
    profit = models.BigIntegerField(blank=True, default=0)

    def save(self, *args, **kwargs):
        # compute profit as (sale * margin) - expenses, keep as integer
        try:
            computed = int(self.sale * PROFIT_MARGIN) - int(self.expenses)
        except Exception:
            computed = 0
        self.profit = computed
        return super().save(*args, **kwargs)

    def __str__(self):

        return str (self.date)