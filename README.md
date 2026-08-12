# J.A.R.V.I.S - Asistente Personal Inteligente

Un asistente personal offline basado en Python que proporciona interfaz de texto y voz, reconocimiento de intenciones (NLP), base de conocimiento local, persistencia de notas y tareas, y más.

## 🎯 Características

✅ **Interfaz CLI interactiva** — Interactúa por texto  
✅ **TTS offline** — Síntesis de voz con `pyttsx3`  
✅ **STT opcional** — Reconocimiento de voz con `SpeechRecognition`  
✅ **NLP básico** — Clasificación de intenciones y manejo de comandos  
✅ **Base de Conocimiento Local** — Indexado TF-IDF con archivos Markdown  
✅ **Notas y Tareas** — Persistencia en JSON  
✅ **Búsqueda Web** — Abre URLs y busca en Google  
✅ **Configuración flexible** — Archivo `config.json` personalizable  

## 📦 Instalación

### Opción A: Desde código fuente

```bash
git clone https://github.com/aaronquijada2008-pixel/J.A.R.V.I.S.git
cd J.A.R.V.I.S
python -m pip install -r requirements.txt
```

### Opción B: Ejecutable Windows (Próximamente)

Descarga `jarvis.exe` desde [Releases](https://github.com/aaronquijada2008-pixel/J.A.R.V.I.S/releases) e ejecuta directamente.

## 🚀 Uso Rápido

### Modo Texto
```bash
python -m jarvis.main
```

### Con Síntesis de Voz
```bash
python -m jarvis.main --voice
```

### Con Reconocimiento de Voz (requiere PyAudio en Windows)
```bash
python -m jarvis.main --listen --voice
```

## 📋 Comandos Disponibles

| Comando | Ejemplo | Descripción |
|---------|---------|-------------|
| `hora` | "¿Qué hora es?" | Muestra la hora actual |
| `abrir` | "Abrir google.com" | Abre URL en navegador |
| `buscar` | "Buscar recetas de paella" | Busca en Google |
| `decir/di` | "Decir hola mundo" | Repite texto en voz |
| `nota` | "Nota comprar leche" | Guarda una nota |
| `notas` | "Mis notas" | Lista notas guardadas |
| `tarea` | "Tarea llamar a mamá" | Crea una tarea |
| `tareas` | "Listar tareas" | Lista tareas pendientes |
| `completar tarea` | "Completar tarea 1" | Marca tarea como hecha |
| `explicar` | "Explicar redes VLAN" | Busca en base de conocimiento |
| `ayuda` | "Ayuda" | Muestra todos los comandos |
| `salir` | "Adiós" | Cierra J.A.R.V.I.S |

## ⚙️ Configuración

Edita `config.json` para personalizar:

```json
{
  "voice": {
    "enabled": true,
    "rate": 150,
    "volume": 0.9
  },
  "speech_recognition": {
    "enabled": false,
    "language": "es-ES"
  },
  "features": {
    "web_search": true,
    "note_taking": true,
    "task_management": true
  }
}
```

## 📚 Base de Conocimiento

Agrega archivos Markdown en la carpeta `knowledge/`:
```
knowledge/
  ├── redes.md
  ├── python.md
  └── welcome.md
```

Luego J.A.R.V.I.S puede buscar y resumir su contenido.

## 🔧 Estructura del Proyecto

```
J.A.R.V.I.S/
├── src/jarvis/
│   ├── main.py           # Entrada principal
│   ├── voice.py          # TTS/STT
│   ├── commands.py       # Manejador de intents
│   ├── storage.py        # Notas/Tareas
│   ├── knowledge.py      # Base de conocimiento
│   └── auth.py           # Autenticación
├── build/
│   ├── jarvis.spec       # Config PyInstaller
│   └── installer.nsi     # Instalador Windows
├── knowledge/            # Base de conocimiento (Markdown)
├── tests/                # Pruebas unitarias
├── config.json          # Configuración del usuario
└── requirements.txt     # Dependencias
```

## 🧪 Pruebas

```bash
pytest tests/ -v
```

## 📦 Distribución

### Generar EXE
```bash
python scripts/build_exe.py
```

### Instalar en Windows
Ejecuta `dist/jarvis_installer.exe` (próximamente)

## 🤖 Arquitectura

### Flujo de Comandos
```
Entrada (texto/voz)
    ↓
Clasificar Intención (IntentClassifier)
    ↓
Ejecutar Handler (handle_command)
    ↓
Respuesta + Persistencia (JSON)
    ↓
Salida (texto/voz)
```

### Módulos Clave

**`commands.py`** — Sistema de intents con patrones regex para clasificación y handlers específicos.

**`knowledge.py`** — Índice TF-IDF de archivos Markdown con búsqueda y resumen automático.

**`storage.py`** — Persistencia de notas y tareas en `jarvis_data.json` con operaciones CRUD.

**`voice.py`** — Encapsulación de `pyttsx3` (TTS) y `SpeechRecognition` (STT).

## 🔐 Seguridad

- Configuración sensible en `config.json` (no commiteada)
- Autenticación por token opcional
- Validación de entrada básica en handlers

## 🐛 Problemas Conocidos

1. **PyAudio en Windows** — Requiere herramientas de compilación. Solución: usar `pipwin install pyaudio` o modo sin audio.
2. **STT limitado** — Solo soporta español con `SpeechRecognition`.
3. **NSIS Installer** — En desarrollo.

## 📝 Roadmap

- [ ] Mejorar detección de intents con ML (sklearn)
- [ ] Agregar integración con APIs externas (weather, news, etc.)
- [ ] Interfaz gráfica (Tkinter/PyQt)
- [ ] Soporte multi-idioma
- [ ] Persistent context y memoria de conversación
- [ ] Plugin system

## 📄 Licencia

MIT

## 👨‍💻 Autor

Aaron Quijada — [GitHub](https://github.com/aaronquijada2008-pixel)

## 🤝 Contribuciones

¡Aceptamos PRs! Abre un issue o PR con sugerencias.

---

**Última actualización:** 2026-08-12  
**Versión:** 0.2.0


Uso por voz:
- Inicia con `--listen --voice` y habla los comandos listados arriba (ej: "explicar J.A.R.V.I.S", "nota comprar leche").

Base de conocimiento:
- Coloca archivos Markdown en la carpeta `knowledge/` (ej: `knowledge/mi_doc.md`).
- Usa `explicar <término>` para que J.A.R.V.I.S busque y resuma información relevante.
- Usa `recargar kb` para reconstruir el índice después de añadir o modificar documentos.

Notas:
- En Windows puede ser necesario instalar PyAudio con `pipwin install pyaudio`.
- Este es un prototipo; ampliar NLP, seguridad e integraciones es el siguiente paso.

Seguridad mínima (token):
- El prototipo soporta una protección simple por token para comandos que modifican datos (notas, tareas, recarga de KB).
- Edita `config.json` en la raíz del proyecto para habilitarla:

```json
{
	"require_token": true,
	"token": "tu_token_seguro"
}
```

- Alternativamente, exporta la variable de entorno `JARVIS_TOKEN` con el valor del token para autorizar sin incrustarlo en el comando.
- También puedes enviar el token como prefijo del comando: `token <tu_token> tarea comprar pan` o `clave <tu_token> nota pagar facturas`.

Scripts incluidos:
- `run_tests.ps1` / `run_tests.sh` — instalan dependencias y ejecutan pruebas (Windows/Linux)
- `run_jarvis.ps1` / `run_jarvis.sh` — ejecutan J.A.R.V.I.S desde la raíz del proyecto

Para ejecutar las pruebas localmente:

```powershell
cd 'C:\Users\David\Desktop\J.A.R.V.I.S'
python -m pip install -r requirements.txt
pytest -q
```

Empaquetado e instalación local:
- Puedes instalar el paquete en editable mode desde la raíz del proyecto:

```powershell
python -m pip install -e .
```

Integración continua:
- Incluimos un workflow de GitHub Actions en `.github/workflows/ci.yml` que ejecuta las pruebas en push/PR.




