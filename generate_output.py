# generate_output.py

import os
import numpy as np
from src.sound_signal import Signal
from src.composite_signal import CompositeSignal
from src.rhythm_signal import RhythmSignal

# Directorio de salida
output_dir = 'output_test'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def generate_signal_output():
    print("\nGenerando señal simple...")
    # Parámetros de la señal simple
    amplitude = 1.0
    freq = 440.0  # A4
    phase = 0.0
    sample_rate = 44100
    duration_seg = 5.0

    # Crear instancia de Signal
    signal = Signal(amplitude, freq, phase, sample_rate, duration_seg)
    signal.generate_signal()

    # Guardar la gráfica y el archivo .wav
    signal.plot_signal(show=False, save_path=os.path.join(output_dir, 'signal_plot.png'))
    signal.save_wav(filename=os.path.join(output_dir, 'signal.wav'))

def generate_composite_signal_output():
    print("\nGenerando señal compuesta...")
    # Crear instancia de CompositeSignal
    composite = CompositeSignal(sample_rate=44100, duration_seg=5.0)

    # Añadir componentes
    composite.add_component(amplitude=1.0, freq=440.0, phase=0.0)      # A4
    composite.add_component(amplitude=0.8, freq=523.25, phase=np.pi/4) # C5
    composite.add_component(amplitude=0.6, freq=659.25, phase=np.pi/2) # E5
    composite.add_component(amplitude=0.5, freq=392.0, phase=np.pi/6)  # G4

    composite.build_signal()

    # Guardar la gráfica y el archivo .wav
    composite.plot_signal(show=False, save_path=os.path.join(output_dir, 'composite_signal_plot.png'))
    composite.save_wav(filename=os.path.join(output_dir, 'composite_signal.wav'))

def generate_rhythm_signal_output():
    print("\nGenerando señal rítmica...")
    # Crear instancia de RhythmSignal
    rhythm = RhythmSignal(sample_rate=44100, duration_seg=5.0, unit_time=1.0)

    # Añadir segmentos de notas o acordes
    rhythm.add_segment([{'amplitude': 1.0, 'freq': 440.0}], label='A4')  # A4
    rhythm.add_segment([{'amplitude': 1.0, 'freq': 493.88}], label='B4') # B4
    rhythm.add_segment([{'amplitude': 1.0, 'freq': 523.25}], label='C5') # C5
    rhythm.add_segment([
        {'amplitude': 1.0, 'freq': 261.63},
        {'amplitude': 1.0, 'freq': 329.63},
        {'amplitude': 1.0, 'freq': 392.0}
    ], label='C Major Chord')                                           # C Major Chord
    rhythm.add_segment([{'amplitude': 1.0, 'freq': 349.23}], label='F4') # F4

    rhythm.build_signal()

    # Guardar la gráfica y el archivo .wav
    rhythm.plot_signal(show=False, save_path=os.path.join(output_dir, 'rhythm_signal_plot.png'))
    rhythm.save_wav(filename=os.path.join(output_dir, 'rhythm_signal.wav'))

if __name__ == "__main__":
    # Generar salidas para cada tipo de señal
    generate_signal_output()
    generate_composite_signal_output()
    generate_rhythm_signal_output()
    print(f"\nResultados guardados en el directorio: {output_dir}")
