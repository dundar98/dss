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

dss.text(r"redirect C:\Users\mu-ha\PycharmProjects\proje\feeders\pv_system.dss")

dss.text(r"redirect C:\Users\mu-ha\PycharmProjects\proje\feeders\storage.dss")

dss.text("set mode = daily")
dss.text("set stepsize = 1h")
dss.text("set number = 1")
#print(dss.circuit.elements_names)
for hour in range(24):
    dss.solution.solve()
    dss.circuit.set_active_element("Load.645")
    vmag_pu = dss.bus.vmag_angle_pu
    print(f" {hour} =  {vmag_pu}")



