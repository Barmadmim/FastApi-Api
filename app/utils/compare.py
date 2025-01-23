import librosa
import numpy as np
from librosa.sequence import dtw
import matplotlib.pyplot as plt

# c:/Users/Admin/OneDrive/Desktop/Api-Micling/app/utils/compare.py

# Cargar dos palabras (como ejemplos)
y1, sr1 = librosa.load('C:/Users/Admin/OneDrive/Desktop/Api-Micling/app/assets/speaking.wav')
y2, sr2 = librosa.load('C:/Users/Admin/OneDrive/Desktop/Api-Micling/app/assets/recording2.wav')

# Extraer MFCC
mfcc1 = librosa.feature.mfcc(y=y1, sr=sr1)
mfcc2 = librosa.feature.mfcc(y=y2, sr=sr2)

# Imprimir las formas de los MFCCs
print(f"Forma MFCC 1: {mfcc1.shape}")
print(f"Forma MFCC 2: {mfcc2.shape}")

# Asegurarte de que las secuencias tengan el mismo número de frames
max_length = min(mfcc1.shape[1], mfcc2.shape[1])
mfcc1 = mfcc1[:, :max_length]
mfcc2 = mfcc2[:, :max_length]

# Transponer las matrices si es necesario
mfcc1 = mfcc1.T
mfcc2 = mfcc2.T

# Imprimir nuevamente para verificar que son compatibles
print(f"Forma final MFCC 1: {mfcc1.shape}")
print(f"Forma final MFCC 2: {mfcc2.shape}")

# Calcular DTW
D, wp = dtw(mfcc1, mfcc2)
print(f"Distancia DTW: {D[-1, -1]}")

# Visualizar la matriz de costos de DTW
plt.imshow(D, origin='lower', aspect='auto', cmap='coolwarm')
plt.colorbar()
plt.title('DTW Cost Matrix')
plt.show()

# Visualizar el camino de alineación
plt.plot(wp[0], wp[1], marker='o')
plt.title('DTW Warping Path')
plt.show()