from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import librosa
import numpy as np
from librosa.sequence import dtw
import os

# Configuración inicial
UPLOAD_FOLDER = "app/assets/uploaded"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Crear el router
audios_router = APIRouter(prefix="/audios", tags=["audios"])

def detectar_silabas(y, sr, top_db=15):
    intervals = librosa.effects.split(y, top_db=top_db)
    print(f"Intervalos detectados: {intervals}")  # Ver los intervalos detectados
    silabas = [y[start:end] for start, end in intervals]
    
    # Filtrar sílabas vacías o demasiado pequeñas
    silabas = [silaba for silaba in silabas if len(silaba) > 0.05 * sr]  # Umbral de longitud mínima
    print(f"Silabas detectadas: {len(silabas)}")  # Ver cuántas sílabas fueron detectadas
    
    return silabas

def calcular_similitud(silaba1, silaba2, sr1, sr2):
    print(f"Calculando similitud entre sílabas de longitudes {len(silaba1)} y {len(silaba2)}")
    
    # Calcular MFCC de ambas sílabas
    mfcc1 = librosa.feature.mfcc(y=silaba1, sr=sr1, n_mfcc=13)
    mfcc2 = librosa.feature.mfcc(y=silaba2, sr=sr2, n_mfcc=13)
    
    print(f"MFCC1 shape: {mfcc1.shape}, MFCC2 shape: {mfcc2.shape}")
    
    # Alinear las longitudes de las sílabas para evitar errores
    min_frames = min(mfcc1.shape[1], mfcc2.shape[1])
    mfcc1 = mfcc1[:, :min_frames].T
    mfcc2 = mfcc2[:, :min_frames].T
    
    # Calcular la distancia DTW
    D, wp = dtw(mfcc1, mfcc2)
    print(f"DTW distance: {D[-1, -1]}")  # Ver la distancia calculada
    return D[-1, -1]

def calcular_porcentaje(distancia, distancia_maxima):
    # Normalizar la distancia a un porcentaje
    return round((1 - (distancia / distancia_maxima)) * 100, 2)

# Endpoint para comparar audios
@audios_router.post("/audios/comparar")
async def comparar_audios(audio1: UploadFile = File(...), audio2: UploadFile = File(...)):
    try:
        # Guardar archivos
        audio1_path = os.path.join(UPLOAD_FOLDER, audio1.filename)
        audio2_path = os.path.join(UPLOAD_FOLDER, audio2.filename)

        with open(audio1_path, "wb") as f:
            f.write(await audio1.read())

        with open(audio2_path, "wb") as f:
            f.write(await audio2.read())

        # Procesar los audios
        y1, sr1 = librosa.load(audio1_path, sr=None)
        y2, sr2 = librosa.load(audio2_path, sr=None)

        # Detectar las sílabas de ambos audios
        silabas1 = detectar_silabas(y1, sr1)
        silabas2 = detectar_silabas(y2, sr2)

        # Comparar las sílabas
        num_silabas = min(len(silabas1), len(silabas2))  # Asegurarse de comparar hasta la mínima cantidad de sílabas
        resultados = []
        
        # Encontrar la distancia máxima para normalizar
        distancias = []
        for i in range(num_silabas):
            distancia = calcular_similitud(silabas1[i], silabas2[i], sr1, sr2)
            distancias.append(distancia)
        
        distancia_maxima = max(distancias) if distancias else 1  # Prevenir división por cero

        # Crear resultados con porcentaje de similitud
        for i in range(num_silabas):
            distancia = distancias[i]
            porcentaje = calcular_porcentaje(distancia, distancia_maxima)
            resultados.append({
                "silaba": i + 1,
                "distancia_dtw": round(distancia, 2),
                "similitud_porcentaje": porcentaje
            })

        return JSONResponse(content={"comparacion": resultados})

    except Exception as e:
        print(f"Error al procesar los audios: {e}")
        return JSONResponse(content={"error": "Error interno en el servidor."}, status_code=500)