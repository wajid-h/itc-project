import random
from datetime import datetime, timedelta
from sales.models import SaleGroup, Sale  # replace 'yourapp' with your app name

# Configuration
business_id = 1  # Replace with your SaleGroup ID
business = SaleGroup.objects.get(id=business_id)

# Generate mock data for 2025
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
delta = timedelta(days=1)

current_date = start_date
while current_date <= end_date:
    sale_amount = round(random.uniform(1000, 5000), 2)
    expenses_amount = round(random.uniform(500, 3000), 2)
    investment_amount = round(random.uniform(0, 2000), 2)

    Sale.objects.create(
        business=business,
        date=current_date,
        sale=sale_amount,
        expenses=expenses_amount,
        investment=investment_amount
    )

    current_date += delta

print("Mock data for 2025 created successfully!")
