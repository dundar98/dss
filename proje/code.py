import matplotlib.pyplot as plt
import py_dss_interface
import os
import pathlib
import random

# DSS dosyasının bulunduğu dizini ve dosya adını ayarlayın
script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("feeders", "13bus", "IEEE13Nodeckt.dss")

# OpenDSS'yi başlatın
dss = py_dss_interface.DSS()

# DSS dosyasını derleyin
dss.text(f"compile [{dss_file}]")
#dss.text(r"redirect C:\Users\mu-ha\PycharmProjects\proje\feeders\storage.dss")
#dss.text(r"redirect C:\Users\mu-ha\PycharmProjects\proje\feeders\pv_system.dss")


# Rastgele tap değeri üretmek için fonksiyon
def generate_random_tap_value():
    return random.randint(-16, 16)

# Düğümlerin gerilim değerlerini al (before optimization)
unoptimized_voltages = []
for phase in range(1, 4):  # Each phase
    unoptimized_voltages.extend(dss.circuit.nodes_vmag_pu_by_phase(phase))

# En küçük uzaklık ve bu uzaklığa ait tap değeri ve gerilimlerin saklanacağı değişkenler
min_distance = float('inf')
best_tap_values = None
best_voltages = None

# 3000 kez işlemi tekrarlayın
for iteration in range(1, 100000):
    # Transformatörleri alma ve next komutu ile adlandırma
    transformer_iterator = dss.transformers.first()
    tap_values = {}
    while transformer_iterator:
        transformer_name = dss.transformers.name
        tap_value = generate_random_tap_value()

        # Tap değerlerini sakla
        tap_values[transformer_name] = tap_value
        dss.transformers._tap_write(tap_value)

        # Bir sonraki transformatöre geçin
        transformer_iterator = dss.transformers.next()

    # DSS'i yeniden çöz
    dss.text("solve")

    # Düğümlerin gerilim değerlerini al
    voltages = []
    for phase in range(1, 4):  # Each phase
        voltages.extend(dss.circuit.nodes_vmag_pu_by_phase(phase))

    # 1'e olan uzaklıkları topla
    total_distance_to_1 = sum([abs(v - 1) for v in voltages])

    # En küçük uzaklığı kontrol et ve gerekirse güncelle
    if total_distance_to_1 < min_distance:
        min_distance = total_distance_to_1
        best_tap_values = tap_values
        best_voltages = voltages

    # Her 100 iterasyonda bir durumu bastır
    if iteration % 100 == 0:
        print(f"Iterasyon: {iteration}, En küçük uzaklık: {min_distance}")

# En iyi tap değerlerini ve bu tap değerlerine karşılık gelen gerilimleri yazdır
print("En küçük uzaklık:", min_distance)
print("En iyi tap değerleri:", best_tap_values)

# Plotting
plt.figure(figsize=(12, 8))

# Plot unoptimized voltages for each phase
plt.subplot(2, 1, 1)
phase_names = ['Phase A', 'Phase B', 'Phase C']
for phase in range(3):  # Each phase
    phase_unoptimized_voltages = unoptimized_voltages[phase::3]
    plt.plot(phase_unoptimized_voltages, label=phase_names[phase])
plt.title('Unoptimized Voltages')
plt.xlabel('Node Index')
plt.axhline(y=1.05, color='red', linestyle='--', label='Upper Bound')
plt.axhline(y=0.95, color='blue', linestyle='--', label='Lower Bound')
plt.ylabel('Voltage (pu)')
plt.legend()

# Plot optimized voltages
plt.subplot(2, 1, 2)
for phase in range(3):  # Each phase
    phase_voltages = best_voltages[phase::3]
    plt.plot(phase_voltages, label=phase_names[phase])
plt.title('Optimized Voltages')
plt.xlabel('Node Index')
plt.ylabel('Voltage (pu)')
plt.axhline(y=1.05, color='red', linestyle='--', label='Upper Bound')
plt.axhline(y=0.95, color='blue', linestyle='--', label='Lower Bound')
plt.legend()

plt.tight_layout()
plt.show()
