# sound_signal.py

import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from .base_signal import BaseSignal
from .utils import normalize_signal

class Signal(BaseSignal):
    def __init__(self, amplitude, freq, phase, sample_rate=44100, duration_seg=5.0):
        super().__init__(sample_rate, duration_seg)
        self.amplitude = amplitude
        self.freq = freq
        self.phase = phase
        self.signal = None

    def generate_signal(self):
        omega = 2 * np.pi * self.freq
        self.signal = self.amplitude * np.cos(omega * self.t + self.phase)
        print(f"Señal generada: {self.amplitude} * cos(2π{self.freq}t + {self.phase})")


    def save_wav(self, filename):
        if self.signal is None:
            raise ValueError("La señal no ha sido generada. Llama a generate_signal() primero.")

        metadata = {
            'amplitude': self.amplitude,
            'freq': self.freq,
            'phase': self.phase,
            'sample_rate': self.sample_rate,
            'duration_seg': self.duration_seg
        }
        super().save_wav(filename=filename, metadata=metadata)

    def plot_signal(self, save_path=None, show=False):
        if self.signal is None:
            print("No se ha generado la señal.")
            return

        plt.figure(figsize=(10, 4))
        period = 1 / self.freq
        max_plot_time = 4 * period
        max_plot_samples = int(max_plot_time * self.sample_rate)
        t_interval = self.t[:max_plot_samples]
        signal_interval = self.signal[:max_plot_samples]

        omega = 2 * np.pi * self.freq
        x_values = omega * t_interval / np.pi

        sns.lineplot(x=x_values, y=signal_interval)
        plt.title(f'Señal: {self.amplitude} * cos(2π{self.freq}t + {self.phase / np.pi:.2f}π)')
        plt.xlabel('ωt / π')
        plt.xticks(ticks=np.linspace(0, 8, 9), labels=[f'{i}π/4' for i in range(9)])
        plt.ylabel('Amplitud')
        plt.ylim([-self.amplitude, self.amplitude])
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
