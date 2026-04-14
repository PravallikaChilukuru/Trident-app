
from django.db import models

class SystemSnapshot(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    uptime = models.CharField(max_length=100)
    cpu_usage = models.FloatField()
    ram_usage = models.FloatField()
    disk_usage = models.FloatField()
    process_count = models.IntegerField()

    def __str__(self):
        return f"Snapshot {self.timestamp.strftime('%Y-%m-%d')}"
