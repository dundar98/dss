import py_dss_interface
import os
import pathlib
import random
import matplotlib.pyplot as plt

# DSS dosyasının bulunduğu dizini ve dosya adını ayarlayın
script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("feeders", "13bus", "IEEE13Nodeckt.dss")

# OpenDSS'yi başlatın
dss = py_dss_interface.DSS()

# DSS dosyasını derleyin
dss.text(f"compile [{dss_file}]")

# Rastgele tap değeri üretmek için fonksiyon
def generate_random_tap_value():
    return random.randint(-16, 16)

# Transformatörleri alma ve next komutu ile adlandırma
transformer_iterator = dss.transformers.first()
for i in range(3000):

    while transformer_iterator:
        transformer_name = dss.cktelement.name  # Transformatör adını almak için bu satırı değiştirin
        tap_value = generate_random_tap_value()

        # Tap değerini güncellemek için OpenDSS komutunu kullanın
        dss.transformers._tap_write(tap_value)
        #Güncellenen tap değerini yazdırın
        print(f"{transformer_name} transformatörünün yeni tap değeri: {tap_value}")

        # Bir sonraki transformatöre geçin
        transformer_iterator = dss.transformers.next()



# DSS çalışma zamanını sonlandırın
dss.text("solve")  # Yeniden çözüm yap

print(dss.circuit.nodes_vmag_pu_by_phase(1))
