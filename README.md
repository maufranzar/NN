# Proyecto de Señales de Sonido y Redes Neuronales con PyTorch

Este proyecto se centra en la generación, análisis y procesamiento de señales de sonido para su uso en redes neuronales utilizando PyTorch. Incluye módulos para crear señales simples, señales compuestas y señales rítmicas, además de herramientas para la normalización, visualización y análisis de componentes de las señales.

## Estructura del Proyecto
.
├── data
│   ├── audio
│   │   ├── chords
│   │   ├── melodies
│   │   ├── notes
│   │   └── superposed
│   └── meta
├── generate_output.py
├── notebooks
│   ├── entrenamiento.ipynb
│   └── generador_frecuencias.ipynb
├── output_test
├── README.md
└── src
    ├── base_signal.py
    ├── composite_signal.py
    ├── __init__.py
    ├── rhythm_signal.py
    ├── sound_signal.py
    └── utils.py


## Requisitos

- Python 3.12 o superior
- Bibliotecas: `numpy`, `matplotlib`, `seaborn`, `scipy`, `librosa`, `pytest`
- PyTorch (si se va a integrar con redes neuronales)

# Pasos:

conda env create -f environment.yml
conda activate audio_project
python -m pip install --upgrade pip
pip install -r requirements.txt

conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
conda install pytorch torchvision torchaudio cpuonly -c pytorch

conda install -c conda-forge librosa
conda install -c anaconda graphviz
pip install pydot
ipython kernel install --user --name=audio_project

---
# Instalar PyTorch (ajusta el comando según tu sistema y si usarás CUDA o no)
conda install pytorch torchvision torchaudio cpuonly -c pytorch

# Instalar torchviz y graphviz
pip install torchviz
conda install -c anaconda graphviz


