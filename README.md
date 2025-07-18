Estructura del proyecto:

```
proyecto-db-local/
│
├── app.py                        # Archivo principal: lanza la app
├── db/
│   └── conexion.py               # Conexión a MongoDB
│
├── controllers/                 # Lógica para manejar los datos
│   └── controller.py            # Funciones CRUD para proyectos
│
├── views/                       # Interfaz gráfica (Tkinter o PyQt)
│   └── interfaz.py              # Ventanas, formularios, filtros
│
├── models/                      # Estructuras de datos (opcional con Mongo)
│   └── proyecto.py              # Definición del esquema esperado
│
├── utils/                       # Funciones auxiliares
│   └── validaciones.py          # Validación de campos, etc.
│
├── requirements.txt             # Lista de dependencias
└── README.md                    # Instrucciones del proyecto

```
