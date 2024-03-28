import py_dss_interface
import os
import pathlib
import matplotlib.pyplot as plt


# DSS dosyasının bulunduğu dizini ve dosya adını ayarlayın
script_path = os.path.dirname(os.path.abspath(__file__))

dss_file = pathlib.Path(script_path).joinpath("feeders", "13bus", "IEEE13Nodeckt.dss")

# OpenDSS'yi başlatın
dss = py_dss_interface.DSS()

# DSS dosyasını derleyin
dss.text(f"compile [{dss_file}]")

dss.text(r"redirect C:\Users\mu-ha\PycharmProjects\proje\feeders\storage.dss")

dss.text(r"redirect C:\Users\mu-ha\PycharmProjects\proje\feeders\pv_system.dss")

dss.text("New Monitor.MonStorage1Powers element=storage.Battery645 mode=1 ppolar=No")

#dss.text("New Monitor.MonPVpowers element=PVSystem.PV645 mode=1 ppolar=No")

dss.text("set mode = daily")
dss.text("set stepsize = 1h")
dss.text("set number = 1")

monitor_values = []

for i in range(24):
    dss.solution.solve()
    monitor_values.append(dss.monitors.channel(1))

# Grafik oluştur
plt.figure(figsize=(12, 8))

# Monitör verilerini grafik olarak çiz
for channel_values in monitor_values:
    plt.plot(channel_values)

# x eksenindeki yazıları dik yazdırma
plt.xticks(rotation=90)
plt.xlabel("Time")
plt.ylabel("Power (kW)")
plt.title("PV Load Shape")
# Grafik gösterme
plt.show()