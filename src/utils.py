# utils.py

import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import seaborn as sns
from scipy.signal import spectrogram


INT16_MAX = 32767

def normalize_signal(signal):
    """
    Normaliza una señal para que sus valores estén dentro del rango [-1, 1].
    """
    max_val = np.max(np.abs(signal))
    if max_val > 1e-8:                  # Añadido un pequeño umbral
        return signal / max_val
    else:
        return signal


def analyze_components(components):
    """
    Muestra un análisis detallado de las componentes de una señal compuesta o rítmica.

    Parámetros:
    - components: Lista de diccionarios que representan componentes de la señal.
    """
    if not components:
        print("No hay componentes para analizar.")
        return

    print("Componentes de la señal:")
    print(f"{'Componente':<12}{'Amplitud':<15}{'Frecuencia (Hz)':<20}{'Fase (π)':<10}")
    for idx, component in enumerate(components):
        phase_pi = component['phase'] / np.pi if 'phase' in component else 0.0
        print(f"{idx + 1:<12}{component['amplitude']:<15.4f}{component['freq']:<20.2f}{phase_pi:<10.2f}")


def plot_spectrogram(signal, sample_rate, save_path=None, max_freq=8000):
    """
    Genera y grafica el espectrograma de una señal, limitando la frecuencia máxima mostrada.
    
    Parámetros:
    - signal: La señal de audio a analizar.
    - sample_rate: La tasa de muestreo de la señal.
    - save_path: Ruta para guardar el espectrograma. Si es None, solo se muestra.
    - max_freq: Frecuencia máxima a mostrar en el espectrograma (en Hz).
    """
    try:
        f, t, Sxx = spectrogram(signal, fs=sample_rate, nperseg=1024, noverlap=512)
        plt.figure(figsize=(10, 6))
        plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud')
        plt.ylabel('Frecuencia [Hz]')
        plt.xlabel('Tiempo [s]')
        plt.colorbar(label='Amplitud [dB]')
        plt.title('Espectrograma')
        plt.ylim(0, max_freq)  # Limitar el eje Y a max_freq Hz
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            print(f'Espectrograma guardado en {save_path}')
        else:
            plt.show()
        plt.close()
    except Exception as e:
        print(f"Error al generar el espectrograma: {e}")



def calculate_note_frequencies(octave_range=(0, 8), ref_freq=440.0):
    """
    Calcula las frecuencias de las notas en el rango de octavas especificado
    utilizando el sistema temperado igual.

    Parámetros:
    - octave_range: Tupla con la octava inicial y final (inclusive).
    - ref_freq: Frecuencia de referencia para A4 (La4), normalmente 440 Hz.

    Retorna:
    - Un diccionario con los nombres de las notas y sus frecuencias.
    """
    note_names = np.array(['C', 'C#', 'D', 'D#', 'E', 'F',
                           'F#', 'G', 'G#', 'A', 'A#', 'B'])
    octaves = np.arange(octave_range[0], octave_range[1] + 1)
    # Número total de notas
    total_notes = len(octaves) * len(note_names)
    # Índices relativos respecto a A4
    note_indices = np.tile(np.arange(len(note_names)), len(octaves))  # shape: (108,)
    octave_offsets = np.repeat(octaves - 4, len(note_names))  # shape: (108,)
    # Cálculo vectorizado de las frecuencias
    note_numbers = octave_offsets * 12 + note_indices - 9  # A4 es la décima nota (índice 9)
    freqs = ref_freq * (2 ** (note_numbers / 12))
    # Crear etiquetas con la misma longitud
    note_labels = np.char.add(np.tile(note_names, len(octaves)), np.repeat(octaves, len(note_names)).astype(str))
    note_frequencies = dict(zip(note_labels, freqs))
    return note_frequencies



def freq_to_note_name(frequency, note_frequencies, tolerance_cents=50):
    """
    Mapea una frecuencia a la nota más cercana dentro de una tolerancia dada en cents.

    Parámetros:
    - frequency: Frecuencia detectada.
    - note_frequencies: Diccionario de notas y sus frecuencias.
    - tolerance_cents: Tolerancia en cents (1 semitono = 100 cents).

    Retorna:
    - El nombre de la nota más cercana o None si ninguna está dentro de la tolerancia.
    """
    if frequency <= 0:
        return None

    notes = np.array(list(note_frequencies.keys()))
    freqs = np.array(list(note_frequencies.values()))
    diff_cents = 1200 * np.log2(frequency / freqs)
    within_tolerance = np.abs(diff_cents) <= tolerance_cents

    if not np.any(within_tolerance):
        return None

    closest_idx = np.argmin(np.abs(diff_cents[within_tolerance]))
    return notes[within_tolerance][closest_idx]


def plot_chromagram(signal, sample_rate, save_path=None, fmax=8000):
    """
    Genera y grafica el chromagram de una señal de audio.

    Parámetros:
    - signal: La señal de audio a analizar.
    - sample_rate: La tasa de muestreo de la señal.
    - save_path: Ruta para guardar el chromagram. Si es None, solo se muestra.
    - fmax: Frecuencia máxima a considerar en el análisis (en Hz).
    """
    try:
        chromagram = librosa.feature.chroma_stft(y=signal, sr=sample_rate, tuning=0, norm=2)
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', sr=sample_rate, cmap='coolwarm')
        plt.colorbar()
        plt.title('Chromagram')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            print(f'Chromagram guardado en {save_path}')
        else:
            plt.show()
        plt.close()
    except Exception as e:
        print(f"Error al generar el chromagram: {e}")