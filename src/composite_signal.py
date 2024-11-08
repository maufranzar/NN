# composite_signal.py

import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from .base_signal import BaseSignal
from .utils import normalize_signal, analyze_components

class CompositeSignal(BaseSignal):
    def __init__(self, sample_rate=44100, duration_seg=5.0):  # Duración predeterminada 5.0
        super().__init__(sample_rate, duration_seg)
        self.components = []
        self.signals = []  # Lista para almacenar señales individuales añadidas

    def add_component(self, amplitude, freq, phase=0.0):
        if freq > self.sample_rate / 2 and freq != 0.0:
            print(f"Advertencia: la frecuencia {freq} Hz supera la mitad de la tasa de muestreo y puede causar aliasing.")
            return
        self.components.append({'amplitude': amplitude, 'freq': freq, 'phase': phase})

    def add_signal(self, signal_instance):
        """
        Añade una señal ya generada a la lista de señales para superposición.
        """
        if signal_instance.signal is None:
            raise ValueError("La señal a añadir no ha sido generada.")
        if len(signal_instance.signal) != len(self.t):
            raise ValueError("La señal añadida no tiene la misma duración que la señal compuesta.")
        self.signals.append(signal_instance.signal)

    def build_signal(self):
        if not self.components and not self.signals:
            raise RuntimeError("No hay componentes ni señales para construir la señal compuesta.")

        composite_signal = np.zeros_like(self.t)

        # Añadir componentes individuales
        for comp in self.components:
            amplitude = comp['amplitude']
            freq = comp['freq']
            phase = comp['phase']
            if freq == 0.0:
                continue  # Placeholder, ya manejamos superposición manualmente
            composite_signal += amplitude * np.cos(2 * np.pi * freq * self.t + phase)

        # Añadir señales superpuestas
        if self.signals:
            composite_signal += np.sum(self.signals, axis=0)

        self.signal = normalize_signal(composite_signal)
        print(f'Señal compuesta generada con {len(self.components)} componentes y {len(self.signals)} señales añadidas.')


    def analyze_components(self):
        analyze_components(self.components)

    def plot_signal(self, show=True, save_path=None):
        if self.signal is None:
            print("No se ha generado la señal compuesta.")
            return

        plt.figure(figsize=(10, 6))
        min_freq = min([comp['freq'] for comp in self.components if comp['freq'] != 0.0], default=1)
        period = 1 / min_freq
        max_plot_time = 4 * period
        max_plot_samples = int(max_plot_time * self.sample_rate)
        t_interval = self.t[:max_plot_samples]
        signal_interval = self.signal[:max_plot_samples]

        omega_min = 2 * np.pi * min_freq
        x_values = omega_min * t_interval / np.pi

        sns.lineplot(x=x_values, y=signal_interval, label='Señal compuesta', color='black')

        # Graficar componentes individuales
        for idx, comp in enumerate(self.components):
            amplitude = comp['amplitude']
            freq = comp['freq']
            phase = comp['phase']
            if freq == 0.0:
                continue  # Placeholder, ya manejamos superposición manualmente
            individual_signal = amplitude * np.cos(2 * np.pi * freq * t_interval + phase)
            sns.lineplot(x=x_values, y=individual_signal, label=f'Componente {idx + 1}: {freq:.2f} Hz')

        # Graficar señales añadidas
        for idx, sig in enumerate(self.signals):
            individual_signal = sig[:max_plot_samples]
            sns.lineplot(x=x_values, y=individual_signal, label=f'Señal añadida {idx + 1}', linestyle='--')

        plt.title(f'Señal compuesta con {len(self.components)} componentes y {len(self.signals)} señales añadidas')
        plt.xlabel('ωt / π')
        plt.xticks(ticks=np.linspace(0, 8, 9), labels=[f'{i}π/4' for i in range(9)])
        plt.ylabel('Amplitud')
        plt.legend(loc='upper right', fontsize='small')
        plt.grid(True)

        if save_path:
            directory = os.path.dirname(save_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            plt.savefig(save_path)
            print(f'Gráfica guardada en {save_path}')
        if show:
            plt.show()
        plt.close()


    def save_wav(self, filename):
        if self.signal is None:
            raise RuntimeError("No se ha generado la señal compuesta.")

        # Preparar metadatos
        metadata = {
            'components': [
                {
                    'amplitude': comp['amplitude'],
                    'freq': comp['freq'],
                    'phase': comp['phase']
                } for comp in self.components
            ],
            'num_signals_added': len(self.signals),
            'sample_rate': self.sample_rate,
            'duration_seg': self.duration_seg
        }

        super().save_wav(filename=filename, metadata=metadata)
