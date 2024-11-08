# base_signal.py

import numpy as np
import os
import json
from scipy.io.wavfile import write
from .utils import normalize_signal, INT16_MAX

class BaseSignal:
    def __init__(self, sample_rate=44100, duration_seg=5.0):
        self.sample_rate = sample_rate
        self.duration_seg = duration_seg
        self.signal = None
        self.t = np.linspace(0, duration_seg, int(sample_rate * duration_seg), endpoint=False)

    def save_wav(self, filename="signal.wav", metadata=None):
        """
        Guarda la señal actual en un archivo WAV e incluye metadatos si se proporcionan.

        Parámetros:
        - filename: Nombre del archivo WAV a guardar.
        - metadata: Diccionario con metadatos para guardar en un archivo JSON asociado.
        """
        if self.signal is None:
            raise RuntimeError("No se ha generado la señal.")

        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Normalizar la señal
        normalized_signal = normalize_signal(self.signal)

        # Convertir a int16
        signal_int = np.int16(normalized_signal * INT16_MAX)

        # Guardar el archivo WAV
        write(filename, self.sample_rate, signal_int)
        print(f'Señal guardada en {filename}')

        # Guardar metadatos si se proporcionan
        if metadata:
            metadata_filename = filename.replace('.wav', '_metadata.json')
            with open(metadata_filename, 'w') as f:
                json.dump(metadata, f, indent=4)
            print(f'Metadatos guardados en {metadata_filename}')

    def plot_signal(self, show=True, save_path=None):
        """
        Método base para graficar la señal. Debe ser implementado por las clases derivadas.

        Parámetros:
        - show: Si es True, muestra la gráfica.
        - save_path: Ruta donde guardar la gráfica. Si es None, no se guarda.
        """
        raise NotImplementedError("El método plot_signal() debe ser implementado por la clase derivada.")
