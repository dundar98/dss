import matplotlib.pyplot as plt

# Verilen sayı dizisi
veri = [0.2, 0.2, 1.5, 1.3, 1.8, 2, 0.2, 0.29, 0.3, 0.3, 0.3, 0.3, 0.3, 0.31, 0.4, 0.38, 0.36, 0.67, 0.7, 0.71, 0.72, 0.73, 0.76, 0.77]

# X ve Y ekseni etiketleri
x_etiketi = 'Time'
y_etiketi = 'Pu'
plt.figure(figsize=(12, 8))

# Grafiği çiz
plt.plot(veri, marker='o')

# Başlık ve ekseni etiketlerini ekle
plt.title('Daily Load Model')
plt.xlabel(x_etiketi)
plt.ylabel(y_etiketi)

# Grafiği göster
plt.show()
