# Gestión de Transporte

Proyecto Django para organizar rutas, viajes, conductores y operadores de una
empresa de transporte.

## Instalación y ejecución

Desde PowerShell, entra a la carpeta del proyecto:

```powershell
cd "C:\Users\sebas\OneDrive\Desktop\gestion de transporte"
```

Si aún no existe el ambiente virtual, se debe crear:

```powershell
python -m venv .venv
```

para activarlo:

```powershell
.\.venv\Scripts\Activate.ps1
```

La activación es correcta cuando aparece `(.venv)` al inicio del terminal.

se instala las dependencias, se aplica las migraciones e inicia el servidor:

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

se abre en el navegador:

- http://127.0.0.1:8000/inicio/ para la página de bienvenida.
- http://127.0.0.1:8000/ruta-inexistente/ para comprobar el error 404.

Para detener el servidor, presiona `CTRL+C`. Para desactivar el ambiente:

```powershell
deactivate
```