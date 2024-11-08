# rhythm_signal.py

import numpy as np
import matplotlib.pyplot as plt
from .composite_signal import CompositeSignal
from .utils import normalize_signal, analyze_components

class RhythmSignal(CompositeSignal):
    def __init__(self, sample_rate=44100, duration_seg=5.0, unit_time=1.0):
        super().__init__(sample_rate, duration_seg)
        self.unit_time = unit_time
        self.segments = []  # Lista para almacenar los segmentos
        self.timeline = []  # Registro temporal de notas

    def add_segment(self, components, label=None):
        current_duration = len(self.segments) * self.unit_time
        if current_duration >= self.duration_seg:
            raise ValueError("Se ha alcanzado la duración total de la señal.")
        self.segments.append(components)

        segment_info = {
            'start_time': current_duration,
            'duration': self.unit_time,
            'components': components,
            'label': label
        }
        self.timeline.append(segment_info)

    def build_signal(self):
        if not self.segments:
            raise RuntimeError("No hay segmentos para construir la señal.")

        self.signal = np.zeros_like(self.t)

        for idx, segment_components in enumerate(self.segments):
            start_time = idx * self.unit_time
            end_time = start_time + self.unit_time
            start_idx = int(start_time * self.sample_rate)
            end_idx = int(end_time * self.sample_rate)
            t_segment = self.t[start_idx:end_idx] - start_time

            if not segment_components:
                continue

            amplitudes = np.array([comp['amplitude'] for comp in segment_components])
            freqs = np.array([comp['freq'] for comp in segment_components])
            phases = np.array([comp.get('phase', 0.0) for comp in segment_components])

            omega = 2 * np.pi * freqs[:, np.newaxis]
            t_matrix = t_segment[np.newaxis, :]

            segment_signals = amplitudes[:, np.newaxis] * np.cos(omega * t_matrix + phases[:, np.newaxis])
            segment_signal = np.sum(segment_signals, axis=0)

            self.signal[start_idx:end_idx] += segment_signal

        self.signal = normalize_signal(self.signal)
        print(f'Señal de ritmo generada con {len(self.segments)} segmentos.')

    def analyze_components(self):
        for segment in self.timeline:
            print(f"Segmento desde {segment['start_time']}s hasta {segment['start_time'] + segment['duration']}s - Label: {segment['label']}")
            analyze_components(segment['components'])
        
        # Opcional: Visualizar la línea de tiempo
        labels = [seg['label'] if seg['label'] else f"Segmento {i+1}" for i, seg in enumerate(self.timeline)]
        start_times = [seg['start_time'] for seg in self.timeline]
        durations = [seg['duration'] for seg in self.timeline]
        
        plt.figure(figsize=(10, 2))
        for i, (start, dur, label) in enumerate(zip(start_times, durations, labels)):
            plt.barh(0, dur, left=start, height=0.3, label=label if label else f"Segmento {i+1}")
        
        plt.xlabel('Tiempo [s]')
        plt.yticks([])
        plt.title('Línea de Tiempo de los Segmentos')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
