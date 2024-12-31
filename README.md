# Proyecto de Generación y Análisis de Ondas Musicales

Este proyecto está enfocado en diseñar y entrenar un modelo híbrido CNN+LSTM utilizando PyTorch para analizar y aprender patrones musicales complejos. Incluye la generación de señales musicales (tonos simples, acordes, melodías) y su análisis utilizando espectrogramas.

---

## **Objetivo Principal**
El objetivo principal es implementar un modelo que combine redes neuronales convolucionales (CNN) y redes neuronales de memoria a largo plazo (LSTM) para extraer características espaciales y temporales de patrones musicales.

---

## **Estructura del Proyecto**
El proyecto está organizado de la siguiente manera:

### **1. Generación de Datos**
- **Directorios**: 
  - `data/` contiene archivos WAV y espectrogramas organizados por carpetas.
- **Tipos de Señales**: 
  - Tonos simples
  - Acordes diatónicos
  - Melodías
  - Progresiones armónicas

### **2. Implementación de Módulos**
Los módulos incluyen:
- `base_signal.py`: Clase base para la generación de señales.
- `sound_signal.py`: Clase para trabajar con señales sonoras simples.
- `composite_signal.py`: Clase para crear señales compuestas.
- `rhythm_signal.py`: Clase para implementar señales rítmicas.
- `utils.py`: Herramientas de apoyo (por ejemplo, visualización y preprocesamiento).

### **3. Arquitectura del Modelo CNN+LSTM**
- **Capas Convolucionales (CNN)**: Para extracción de características espaciales.
- **Capas LSTM**: Para aprendizaje de dependencias temporales.
- **Capa Totalmente Conectada**: Para clasificación.

### **4. Preprocesamiento y Carga de Datos**
- **Dataset Personalizado**: 
  - Clase `AudioDataset` para cargar espectrogramas organizados por carpetas.
- **Transformaciones**: 
  - Redimensionamiento, normalización y conversión a tensores.
- **DataLoader**: 
  - División en conjuntos de entrenamiento (80%) y validación (20%).

### **5. Entrenamiento y Evaluación del Modelo**
- **Función de Entrenamiento**: 
  - `train_model`: Ejecuta el ciclo de entrenamiento y validación.
- **Optimización**: 
  - Uso de `CrossEntropyLoss` como función de pérdida y `Adam` como optimizador.
- **Métricas**: 
  - Seguimiento de pérdida y precisión por época.

---

## **Uso del Proyecto**

### **Requisitos Previos**
- Python 3.8+
- PyTorch 1.10+
- Librerías adicionales: `torchvision`, `numpy`, `matplotlib`, `torchsummary`, `torchviz`.

### **Instalación**
1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/proyecto-musical.git
   cd proyecto-musical
   ```
2. Instala los requisitos:
   ```bash
   pip install -r requirements.txt
   ```

### **Ejecución**
1. Genera datos:
   ```bash
   python generate_data.py
   ```
2. Entrena el modelo:
   ```bash
   python train_model.py
   ```
3. Visualiza resultados:
   - Diagrama del modelo: Utiliza `torchviz`.
   - Arquitectura resumida: Usa `torchsummary`.

---

## **Resultados Esperados**
- Un modelo entrenado capaz de analizar patrones musicales complejos.
- Espectrogramas y gráficos que visualicen las características extraídas.
- Métricas como precisión y pérdida a lo largo del entrenamiento.

---

## **Plan Futuro**
1. Culminar la etapa de entrenamiento y evaluación del modelo.
2. Documentar el proyecto completo.
3. Explorar aplicaciones prácticas, como transcripción musical y asistentes de composición.

---

## **Notas Adicionales**
- Algunos problemas con archivos sin sonido podrían estar relacionados con la carga de procesamiento paralela durante la generación de datos o el entrenamiento.
- Asegúrate de tener suficientes recursos computacionales para evitar interrupciones.

---

## **Licencia**
Este proyecto se encuentra bajo la licencia MIT. Para más detalles, consulta el archivo `LICENSE`.

---

## **Contacto**
Mauricio Franco  
[Tu Sitio Web](http://mauranzar.com)  
Correo: mauricio@example.com
