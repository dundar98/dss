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

dss.text("New Monitor.MonStorage1Powers element=storage.Battery645 mode=1 ppolar=No")

dss.text(r"redirect C:\Users\mu-ha\PycharmProjects\proje\feeders\pv_system.dss")


dss.text("set mode = daily")
dss.text("set stepsize = 1h")
dss.text("set number = 1")

plt.figure(figsize=(12, 8))

for i in range(24):
    dss.solution.solve()
    #print(i)
    plt.plot(dss.circuit.nodes_names_by_phase(1),dss.circuit.nodes_vmag_pu_by_phase(1))
    #print(dss.circuit.buses_vmag_pu)
# x eksenindeki yazıları dik yazdırma
plt.xticks(rotation=45)
plt.axhline(y=1.05, color='red', linestyle='--', label='Upper Bound')
plt.axhline(y=0.95, color='blue', linestyle='--', label='Lower Bound')
# Grafik gösterme
plt.show()
