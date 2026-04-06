from django.shortcuts import render, redirect
from .models import Vehicle
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import math
import string
from django.utils.timezone import now
from django.contrib.auth.models import User

# SendGrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def get_vip_slot():
    for letter in string.ascii_uppercase[:20]:
        for num in range(1, 6):
            slot = f"{letter}{num}"
            if not Vehicle.objects.filter(slot=slot, floor="F3", exit_time=None).exists():
                return slot
    return None


def get_car_slot():
    for letter in string.ascii_uppercase[:20]:
        for num in range(1, 6):
            slot = f"{letter}{num}"
            if not Vehicle.objects.filter(slot=slot, vehicle_type="car", is_vip=False, exit_time=None).exists():
                return slot
    return None


def get_bike_slot():
    for letter in string.ascii_uppercase[:20]:
        for num in range(1, 11):
            slot = f"{letter}{num}"
            if not Vehicle.objects.filter(slot=slot, vehicle_type="bike", is_vip=False, exit_time=None).exists():
                return slot
    return None


def get_floor(vtype, vip):
    if vip:
        return "F3"

    if vtype == "car":
        count = Vehicle.objects.filter(vehicle_type="car", is_vip=False, exit_time=None).count()
        return "F1" if count < 100 else "F2"

    return "F4"


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def entry(request):
    if request.method == "POST":
        vtype = request.POST['type']
        number = request.POST['number']
        email = request.POST['email']
        vip = request.POST.get('vip') == "yes"

        if vip:
            slot = get_vip_slot()
        else:
            slot = get_car_slot() if vtype == "car" else get_bike_slot()

        if slot is None:
            return render(request, "entry.html", {"error": "Parking Full"})

        floor = get_floor(vtype, vip)

        vehicle = Vehicle.objects.create(
            vehicle_number=number,
            vehicle_type=vtype,
            is_vip=vip,
            slot=slot,
            floor=floor,
            email=email
        )

        message = f"""
Parking Ticket

Ticket ID: {vehicle.ticket_id}
Vehicle: {vehicle.vehicle_number}
Slot: {vehicle.slot}
Floor: {vehicle.floor}
Entry Time: {vehicle.entry_time}
"""

        # ✅ SEND EMAIL WITH DEBUG
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

            email_msg = Mail(
                from_email='your_verified_sendgrid_email',
                to_emails='jeffkishore19@gmail.com',  # TEMP test email
                subject='Parking Ticket',
                plain_text_content=message
            )

            response = sg.send(email_msg)
            print("EMAIL STATUS:", response.status_code)

        except Exception as e:
            print("EMAIL ERROR:", e)

        return render(request, "success.html", {"v": vehicle})

    return render(request, "entry.html")


@login_required
def exit(request):
    if request.method == "POST":
        ticket = request.POST['ticket']
        exit_time_input = request.POST['exit_time']

        try:
            vehicle = Vehicle.objects.get(ticket_id=ticket)
        except:
            return render(request, "exit.html", {"error": "Invalid Ticket"})

        entry_time = vehicle.entry_time

        exit_time = datetime.strptime(exit_time_input, "%H:%M")
        exit_time = entry_time.replace(hour=exit_time.hour, minute=exit_time.minute)

        seconds = (exit_time - entry_time).total_seconds()

        if seconds <= 0:
            return render(request, "exit.html", {"error": "Invalid Time"})

        hours = math.ceil(seconds / 3600)

        if vehicle.is_vip:
            bill = 70 if hours <= 1 else 70 + (hours - 1) * 15
        else:
            bill = 40 if hours <= 1 else 40 + (hours - 1) * 15

        vehicle.exit_time = exit_time
        vehicle.total_hours = hours
        vehicle.bill = bill
        vehicle.save()

        return render(request, "bill.html", {"v": vehicle})

    return render(request, "exit.html")


def login_view(request):
    user_obj, created = User.objects.get_or_create(username="parkingadmin")

    user_obj.set_password("parking123")
    user_obj.email = "jeffkishore19@gmail.com"
    user_obj.is_superuser = True
    user_obj.is_staff = True
    user_obj.save()

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/home/')
        else:
            return render(request, "login.html", {"error": "Invalid login"})

    return render(request, "login.html")


@login_required
def slots(request):
    parked = Vehicle.objects.filter(exit_time=None)
    occupied = set(f"{v.slot}_{v.floor}" for v in parked)

    floors = {}

    for floor in ["F1", "F2", "F3"]:
        grid = []
        for letter in string.ascii_uppercase[:20]:
            row = []
            for num in range(1, 6):
                slot = f"{letter}{num}"
                key = f"{slot}_{floor}"
                status = "occupied" if key in occupied else "empty"
                row.append((slot, status))
            grid.append(row)
        floors[floor] = grid

    grid = []
    for letter in string.ascii_uppercase[:20]:
        row = []
        for num in range(1, 11):
            slot = f"{letter}{num}"
            key = f"{slot}_F4"
            status = "occupied" if key in occupied else "empty"
            row.append((slot, status))
        grid.append(row)

    floors["F4"] = grid

    return render(request, "slots.html", {"floors": floors})


@login_required
def dashboard(request):
    today = now().date()
    vehicles = Vehicle.objects.filter(entry_time__date=today)

    context = {
        "car_count": vehicles.filter(vehicle_type="car").count(),
        "bike_count": vehicles.filter(vehicle_type="bike").count(),
        "vip_count": vehicles.filter(is_vip=True).count(),
    }

    return render(request, "dashboard.html", context)