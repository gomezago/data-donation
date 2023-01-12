from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import DataSlipDonation
from django.db.models import Sum


# Create your views here.
def atm(request):
    # Transport: Personal Card (e.g., NS)
    request.session['transport'] = False
    # Supermarket: Loyalty Card
    request.session['supermarket'] = False
    # Shopping: Credit Card
    request.session['card'] = False
    # Body: Smartwatch, Smart ring
    request.session['smartwatch'] = False
    request.session['ring'] = False
    # Apps:
    request.session['weather'] = False
    request.session['navigation'] = False
    request.session['browser'] = False
    request.session['email'] = False
    request.session['whatsapp'] = False
    request.session['spotify'] = False
    request.session['social'] = False
    request.session['dating'] = False
    request.session['tracking'] = False
    print(request.session.values())
    return render(request, 'atm.html')

def atm_transport(request):
    print(request.session.values())
    return render(request, 'atm_transport.html')

def atm_food(request):
    if request.POST.get("transport") == '1':
        request.session['transport'] = True
    print(request.session.values())
    return render(request, "atm_food.html")

def atm_pay(request):
    if request.POST.get("supermarket") == '1':
        request.session["supermarket"] = True
    print(request.session.values())
    return render(request, "atm_pay.html")

def atm_body(request):
    if request.POST.get("card") == '1':
        request.session["card"] = True
    print(request.session.values())
    return render(request, "atm_body.html",)

def atm_phone(request):
    if request.POST.get("smartwatch") == "on":
        request.session["smartwatch"] = True
    if request.POST.get("ring") == "on":
        request.session["ring"] = True
    print(request.session.values())
    return render(request, "atm_phone.html",)

def atm_donate(request):
    if request.POST.get("navigation") == "on":
        request.session["navigation"] = True
    else:
        request.session["navigation"] = False
    if request.POST.get("weather") == "on":
        request.session["weather"] = True
    else:
        request.session["weather"] = False
    if request.POST.get("browser") == "on":
        request.session["browser"] = True
    else:
        request.session["browser"] = False
    if request.POST.get("email") == "on":
        request.session["email"] = True
    else:
        request.session["email"] = False
    if request.POST.get("whatsapp") == "on":
        request.session["whatsapp"] = True
    else:
        request.session["whatsapp"] = False
    if request.POST.get("spotify") == "on":
        request.session["spotify"] = True
    else:
        request.session["spotify"] = False
    if request.POST.get("social") == "on":
        request.session["social"] = True
    else:
        request.session["social"] = False
    if request.POST.get("dating") == "on":
        request.session["dating"] = True
    else:
        request.session["dating"] = False
    if request.POST.get("tracking") == "on":
        request.session["tracking"] = True
    else:
        request.session["tracking"] = False
    print(request.session.values())
    return render(request, "atm_donate.html",)

def atm_printing(request):
    print(request.session.values())
    if request.POST.get("donate"):

        wearable_list = [request.session['smartwatch'], request.session['ring']]

        app_list = [request.session["navigation"], request.session["weather"], request.session["browser"],
                    request.session["email"], request.session["whatsapp"], request.session["spotify"],
                    request.session["social"], request.session["dating"], request.session["tracking"]]

        new_donation = DataSlipDonation(
            transport = request.session["transport"],
            supermarket = request.session["supermarket"],
            card = request.session["card"],
            wearable = any(wearable_list),
            apps = any(app_list),
        )
        new_donation.save()

    print(request.session.values())
    return render(request, 'atm_print.html')

def receipt(request):
    print(request.session.values())
    return render(request, 'receipt.html')