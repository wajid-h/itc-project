from django.shortcuts import render, redirect
from .models import Sale, SaleGroup
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import error
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Max, Min, Count
from .models import SaleGroup, Sale
from django.utils.dateparse import parse_date

@login_required
def sales_report(request, id):
    
    business = get_object_or_404(
        SaleGroup,
        id=id,
        owner=request.user
    )

    start_date = request.GET.get("start")
    end_date = request.GET.get("end")

    sales_qs = business.sales.all()

    if start_date and end_date:
        sales_qs = sales_qs.filter(
            date__date__range=[start_date, end_date]
        )

    summary = sales_qs.aggregate(
        gross_revenue=Sum("sale"),
        total_expenses=Sum("expenses"),
        total_profit=Sum("profit"),
        avg_sale=Avg("sale"),
        max_sale=Max("sale"),
        min_sale=Min("sale"),
        total_sales=Count("id"),
    )

    # Daily aggregation for charts
    from django.db.models import F
    from django.db.models.functions import TruncDate
    
    daily_data = sales_qs.annotate(
        sale_date=TruncDate("date")
    ).values("sale_date").annotate(
        daily_revenue=Sum("sale"),
        daily_expenses=Sum("expenses"),
        daily_profit=Sum("profit"),
        transaction_count=Count("id")
    ).order_by("sale_date")

    # Format for Chart.js
    dates = [d["sale_date"].strftime("%b %d") for d in daily_data]
    revenues = [float(d["daily_revenue"] or 0) for d in daily_data]
    expenses = [float(d["daily_expenses"] or 0) for d in daily_data]
    profits = [float(d["daily_profit"] or 0) for d in daily_data]

    context = {
        "business": business,
        "summary": summary,
        "start_date": start_date,
        "end_date": end_date,
        "chart_dates": dates,
        "chart_revenues": revenues,
        "chart_expenses": expenses,
        "chart_profits": profits,
        "bid" : id
    }   

    return render(request, "sales_report.html", context)


def index(request):
    if request.user.is_authenticated == True:
        return redirect("groups")
    return render(request, "index.html")

def groups(request):
    if request.user.is_authenticated != True:
            return redirect("login")

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        if name and description:
            SaleGroup.objects.create(
                name=name,
                description=description,
                owner=request.user
            )
        

        return redirect("index")  

    return render(request, "groups.html")

def index_business(request, id):

    if not request.user.is_authenticated:
        return redirect("login")

    business = SaleGroup.objects.get(id=id)
    sales = business.sales.all()

    for s in sales :
        s.refresh_profit();
    
    if request.method == "POST":
        date = request.POST.get("date")
        sale = request.POST.get("sale")
        expenses = request.POST.get("expenses")
        investment = request.POST.get("investment")

        sale = Sale.objects.create(
            business=business,
            date=date,
            sale=sale,
            expenses=expenses,
            investment=investment
        )

        sale.save();    
        return redirect("index-business", id=id)

    return render(request, "index_sales.html", {
        "sales": sales,
        "bid": id
    })

def front_logout(request):
    logout(request)
    return redirect("login")


def onboard(request):
    print("preparing auth   ...")

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        action = request.POST.get("is_login")  # 'login' or 'signup' expected

        if action == "login":
            login_email = request.POST.get("login_email", "")
            login_password = request.POST.get("login_password", "")

            try:
                target_user = User.objects.get(email=login_email)
            except User.DoesNotExist:
                error(request, "No registered accounts with that email address.")
                return redirect("login")

            user = authenticate(request, username=target_user.username, password=login_password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                error(request, "Password entered for that account is invalid.")
                return redirect("login")

        elif action == "signup":
            fullName = request.POST.get("name", "").strip()
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "")
            conf_pass = request.POST.get("conf_password", "")

            if User.objects.filter(email=email).exists():
                error(request, "An account with that email exists. Perhaps you want to login?")
                return redirect("login")
            if User.objects.filter(username=username).exists():
                error(request, "That username is already in use.")
                return redirect("login")

            if password != conf_pass:
                error(request, "Passwords don't match.")
                return redirect("login")

            if len(password) < 5:
                error(request, "Password should be at least 5 characters long.")
                return redirect("login")

            new_user = User(email=email, first_name=fullName, username=username)
            new_user.set_password(conf_pass)
            new_user.save()

            user = authenticate(request, username=username, password=conf_pass)
            if user:
                login(request, user)
                return redirect('index')
            else:
                login(request, new_user)
                return redirect('index')

    return render(request, "onboard.html")


