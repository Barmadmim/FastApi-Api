import librosa
import librosa.display
import numpy as np
from librosa.sequence import dtw
import matplotlib.pyplot as plt
import math

# Función para detectar sílabas
def detectar_silabas(audio_path, top_db=15):
    y, sr = librosa.load(audio_path)
    intervals = librosa.effects.split(y, top_db=top_db)
    silabas = [y[start:end] for start, end in intervals]
    tiempos = [(start / sr, end / sr) for start, end in intervals]
    return silabas, tiempos, sr

# Función para calcular DTW entre dos sílabas
def calcular_similitud(silaba1, silaba2, sr1, sr2):
    mfcc1 = librosa.feature.mfcc(y=silaba1, sr=sr1, n_mfcc=13)
    mfcc2 = librosa.feature.mfcc(y=silaba2, sr=sr2, n_mfcc=13)

    min_frames = min(mfcc1.shape[1], mfcc2.shape[1])
    mfcc1 = mfcc1[:, :min_frames].T
    mfcc2 = mfcc2[:, :min_frames].T

    D, wp = dtw(mfcc1, mfcc2)
    return D[-1, -1]

# Cargar y detectar sílabas
silabas1, tiempos1, sr1 = detectar_silabas('C:/Users/Admin/OneDrive/Desktop/Api-Micling/app/assets/speaking.wav')
silabas2, tiempos2, sr2 = detectar_silabas('C:/Users/Admin/OneDrive/Desktop/Api-Micling/app/assets/recording2.wav')

# Comparar sílabas
print("\nComparación de sílabas:")
num_silabas = min(len(silabas1), len(silabas2))
for i in range(num_silabas):
    distancia = calcular_similitud(silabas1[i], silabas2[i], sr1, sr2)
    print(f"Sílaba {i + 1}: Distancia DTW = {distancia:.2f}")

# Configurar filas y columnas
num_columnas = 3
num_filas = math.ceil(num_silabas * 2 / num_columnas)

plt.figure(figsize=(num_columnas * 4, num_filas * 4))

# Graficar las sílabas de ambos audios en posiciones consecutivas
for i in range(num_silabas):
    # Sílaba del primer audio
    plt.subplot(num_filas, num_columnas, 2 * i + 1)
    librosa.display.waveshow(silabas1[i], sr=sr1)
    plt.title(f"Audio 1 - Sílaba {i + 1}")

    # Sílaba del segundo audio
    plt.subplot(num_filas, num_columnas, 2 * i + 2)
    librosa.display.waveshow(silabas2[i], sr=sr2)
    plt.title(f"Audio 2 - Sílaba {i + 1}")

plt.tight_layout()
plt.show()
