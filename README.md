J.A.R.V.I.S - Asistente personal (prototipo)


Proyecto mínimo en Python para un asistente local llamado J.A.R.V.I.S.

Características incluidas:
- Interfaz CLI interactiva
- TTS offline con `pyttsx3`
- Reconocimiento de voz (opcional) con `SpeechRecognition`
- Manejo de comandos y NLP básico (intenciones)
- Base de conocimiento local (Markdown) con indexado TF-IDF
- Persistencia simple de notas y tareas (JSON)

Instalación rápida:

```powershell
python -m pip install -r requirements.txt
```

Ejecutar (modo texto):

```powershell
python -m jarvis.main
```

Ejecutar con TTS:

```powershell
python -m jarvis.main --voice
```

Ejecutar con escucha por micrófono (opcional, requiere dependencias del sistema para PyAudio):

```powershell
python -m jarvis.main --listen --voice
```

Comandos principales (ejemplos):
- `hora` — muestra la hora actual
- `abrir <url>` — abre una URL en el navegador
- `buscar <texto>` — busca en la web
- `decir <texto>` — repite el texto
- `nota <texto>` — guarda una nota
- `recordar` / `notas` — lista notas guardadas
- `tarea <texto>` — crea una tarea
- `listar tareas` — lista tareas
- `completar tarea <id>` — marca una tarea como hecha
- `explicar <tema>` / `qué es <tema>` — busca en la base de conocimiento local y devuelve un resumen
- `recargar kb` / `recargar` — recarga el índice de la base de conocimiento

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




