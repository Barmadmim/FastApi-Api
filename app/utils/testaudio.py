# Archivo: app/utils/audio_similarity.py

# Importar librerías necesarias
import librosa
import os
import numpy as np
from torch import no_grad
from transformers import Wav2Vec2Processor, Wav2Vec2Model
from sklearn.metrics.pairwise import cosine_similarity

# Función para cargar y normalizar audio
def load_audio(file_path, sr=16000, max_duration=None):
    """
    Carga y normaliza un archivo de audio.

    Args:
        file_path (str): Ruta del archivo de audio.
        sr (int): Frecuencia de muestreo deseada (default: 16kHz).
        max_duration (float): Duración máxima en segundos (opcional).

    Returns:
        np.ndarray: Señal de audio normalizada.
    """
    audio, _ = librosa.load(file_path, sr=sr, duration=max_duration)
    audio = librosa.util.normalize(audio)
    return audio

# Función para extraer embeddings de audio usando Wav2Vec 2.0
def extract_embeddings(audio, processor, model, sr=16000, chunk_size=16000):
    """
    Extrae los embeddings de audio usando Wav2Vec2.

    Args:
        audio (np.ndarray): Señal de audio.
        processor: Procesador Wav2Vec2.
        model: Modelo Wav2Vec2.
        sr (int): Frecuencia de muestreo.
        chunk_size (int): Tamaño de los fragmentos en samples.

    Returns:
        list: Lista de embeddings de los fragmentos.
    """
    embeddings = []
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i+chunk_size]
        inputs = processor(chunk, sampling_rate=sr, return_tensors="pt", padding=True)
        with no_grad():
            embeddings.append(model(**inputs).last_hidden_state)
    return embeddings

# Función para calcular similitud entre embeddings
def calculate_similarity(embeddings_ref, embeddings_user):
    """
    Calcula la similitud coseno entre dos sets de embeddings.

    Args:
        embeddings_ref (list): Embeddings del audio de referencia.
        embeddings_user (list): Embeddings del audio de usuario.

    Returns:
        list: Similitudes calculadas por fragmento.
    """
    similarities = []
    for ref, user in zip(embeddings_ref, embeddings_user):
        sim = cosine_similarity(ref.mean(dim=0).reshape(1, -1), user.mean(dim=0).reshape(1, -1))
        similarities.append(sim[0][0])
    return similarities

# Función principal para comparar audios
def compare_audios(ref_audio_path, user_audio_path):
    """
    Compara dos archivos de audio calculando su similitud.

    Args:
        ref_audio_path (str): Ruta del audio de referencia.
        user_audio_path (str): Ruta del audio de usuario.

    Returns:
        list: Similitudes por fragmento.
    """
    if not os.path.exists(ref_audio_path) or not os.path.exists(user_audio_path):
        raise FileNotFoundError("Uno o ambos archivos de audio no existen.")

    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h", trust_remote_code=True)
    model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h", trust_remote_code=True)

    ref_audio = load_audio(ref_audio_path)
    user_audio = load_audio(user_audio_path)

    embeddings_ref = extract_embeddings(ref_audio, processor, model)
    embeddings_user = extract_embeddings(user_audio, processor, model)

    return calculate_similarity(embeddings_ref, embeddings_user)

# Ejecución principal
if __name__ == "__main__":
    ref_audio_path = "./app/utils/audio_ref.wav"
    user_audio_path = "./app/utils/audio_user.wav"

    try:
        results = compare_audios(ref_audio_path, user_audio_path)
        print("Resultados de similitud por sílaba:")
        for idx, sim in enumerate(results):
            print(f"- Sílaba {idx + 1}: {sim * 100:.2f}% de precisión")
        print(f"\nPrecisión promedio: {np.mean(results) * 100:.2f}%")
    except Exception as e:
        print(f"Error: {e}")
