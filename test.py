
import psutil


for item in psutil.disk_partitions():
    print(item)
