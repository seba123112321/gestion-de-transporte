# Gestión de Transporte

Proyecto Django para administrar rutas, conductores, operadores y viajes mediante
una API REST con Django REST Framework.

## Requisitos

- Python 3.13 o compatible con Django 5.2/6.1.
- MySQL 8. SQLite queda disponible como alternativa para desarrollo local.

## Instalación y configuración

Desde PowerShell, en la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` y define una clave `SECRET_KEY` propia, las credenciales de la base
de datos y `ALLOWED_HOSTS`. Puedes generar una clave con:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

No publiques `.env` ni sus credenciales.

Para desarrollo local con `runserver`, deja `DEBUG=True` para que Django sirva
los estilos y scripts del administrador. En producción, usa `DEBUG=False` y
configura un servidor de archivos estáticos.

MySQL es la base de datos predeterminada. Antes de iniciar Django, ajusta el
nombre de usuario y la contraseña tanto en `.env` como en
`scripts/sql/setup_mysql.sql`, y ejecuta ese script desde MySQL Workbench con una
cuenta administradora de MySQL. Los valores `DB_NAME`, `DB_USER`, `DB_PASSWORD`,
`DB_HOST` y `DB_PORT` de `.env` deben coincidir con la base y el usuario creados.

Para usar SQLite en vez de MySQL, configura en `.env`:

```dotenv
DB_ENGINE=sqlite
DB_NAME=./db.sqlite3
```

Aplica migraciones e inicia el servidor:

```powershell
python manage.py migrate
python manage.py runserver
```

## API CRUD

La raíz del router muestra los recursos disponibles en `http://127.0.0.1:8000/api/`.
Cada recurso admite `GET` de colección/detalle, `POST`, `PUT`, `PATCH` y `DELETE`:

| Recurso | Endpoint |
| --- | --- |
| Rutas | `/api/rutas/` |
| Conductores | `/api/conductores/` |
| Operadores | `/api/operadores/` |
| Viajes | `/api/viajes/` |

## Modelo de datos

- **Ruta:** nombre, origen, destino, distancia positiva en kilómetros y estado
  activo.
- **Conductor:** nombre, licencia única, teléfono opcional y estado activo.
- **Operador:** nombre, correo opcional y único, teléfono opcional y estado
  activo.
- **Viaje:** referencias obligatorias a una ruta, un conductor y un operador;
  fechas de salida y llegada opcional; estado programado, en curso, completado
  o cancelado.

Todos los modelos guardan fecha de creación y actualización. Las rutas,
conductores y operadores no se pueden eliminar mientras tengan viajes asociados;
la API responde con HTTP 409 en ese caso. La llegada de un viaje, si se informa,
debe ser posterior a su salida.

La interfaz de bienvenida está en `/inicio/`. Una URL inexistente, como
`/ruta-inexistente/`, muestra la página 404 personalizada.

## Pruebas

```powershell
python manage.py test
```

La API permite acceso sin autenticación para facilitar esta evaluación académica.
Antes de desplegarla en producción, configura autenticación, permisos restrictivos
y una clave/credenciales propias.
