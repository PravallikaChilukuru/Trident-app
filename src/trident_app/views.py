import datetime
import psutil
import subprocess
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from .models import SystemSnapshot
from dotenv import load_dotenv
load_dotenv()


def get_uptime():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    return str(uptime).split('.')[0]

def vm_health(request):
    vms = {
        "Web-Server": os.getenv('IP_WEB_SERVER'),
        "App-Server": os.getenv('IP_JUMP_HOST'),
        "DB-Server": os.getenv('IP_DB_SERVER')
    }
    results = {}

    for name, ip in vms.items():
        res = subprocess.call(['ping', '-c', '1', '-W', '1', ip],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        results[name] = "UP" if res == 0 else "DOWN"

    latest_snapshot = SystemSnapshot.objects.order_by('-timestamp').first()
    audit_time = latest_snapshot.timestamp.strftime('%Y-%m-%d') if latest_snapshot else "No Data"
    try:
       db_conn = connections['default']
       db_conn.cursor()
       results["Database-Service"] = "UP"
    except OperationalError:
        results["Database-Service"] = "DOWN"
    
    except OperationalError:
        results["Database-Service"] = "DISCONNECTED"
    metrics = {
        "uptime": get_uptime(),
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "processes": len(psutil.pids()),
    }
    today = datetime.date.today()
    if not SystemSnapshot.objects.filter(timestamp__date=today).exists():
        SystemSnapshot.objects.create(
             uptime=metrics["uptime"],
             cpu_usage=metrics["cpu"],
             ram_usage=metrics["ram"],
             disk_usage=metrics["disk"],
             process_count=metrics["processes"]
       )
    
    if request.GET.get('format') == 'json':
        return JsonResponse(results)
    return render(request, 'dashboard.html', {
        'results': results, 
        'audit_time': audit_time
    })
