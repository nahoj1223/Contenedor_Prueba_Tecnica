# Contenedor Prueba Técnica

Este proyecto implementa una arquitectura de microservicios con FastAPI y PostgreSQL para la gestión de productos y precios, incluyendo países y cupones de descuento.

## Estructura de Microservicios

- **microservicio1:** Gestión de productos.
- **microservicio2:** Gestión de precios, países y cupones.
- **init-scripts:** Scripts SQL para inicializar las bases de datos.
- **docker-compose.yml:** Orquestación de servicios y bases de datos.

## Tecnologías

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker & Docker Compose

## Levantar el Proyecto

1. **Clona el repositorio:**
   ```sh
   git clone <url-del-repo>
   cd Contenedor_Prueba_Tecnica
   ```

2. **Levanta los servicios con Docker Compose:**
   ```sh
   docker-compose up --build
   ```

   Esto iniciará:
   - microservicio1 en el puerto `8000`
   - microservicio2 en el puerto `8001`
   - Bases de datos PostgreSQL en los puertos `5432` y `5433`
   - PgAdmin en el puerto `80`

3. **Accede a la documentación interactiva:**
   - [http://localhost:8000/docs](http://localhost:8000/docs) (Productos)
   - [http://localhost:8001/docs](http://localhost:8001/docs) (Precios)

## Endpoints Principales

### microservicio1 (Productos)
- `POST /products` - Crear producto
- `GET /products/list` - Listar productos
- `GET /products/{sku}` - Consultar producto por SKU
- `PUT /products/{sku}` - Actualizar producto
- `DELETE /products/{sku}` - Eliminar producto

### microservicio2 (Precios)
- `POST /pricing/quote` - Calcular precio final de producto (incluye país y cupón)
- `GET /health` - Verificar estado del microservicio

## Arquitectura

- **Domain:** Entidades, repositorios y casos de uso.
- **Infrastructure:** Implementaciones de repositorios, modelos de base de datos y mapeadores.
- **API:** Rutas y controladores FastAPI.
- **Core:** Configuración de base de datos y logging.
- **Schemas:** Validación y serialización con Pydantic.
- **Utils:** Utilidades comunes (respuestas estándar).

## Variables de Entorno

Configura las variables de conexión en los archivos `.env` de cada microservicio.

## Inicialización de Base de Datos

Los scripts en `init-scripts/` crean las tablas y datos iniciales para productos, países y cupones.

## Pruebas

Las pruebas unitarias y de integración están organizadas por microservicio:

- `microservicio1/tests/`: Pruebas para los endpoints de productos.
- `microservicio2/tests/`: Pruebas para los endpoints de precios

### Ejecutar pruebas localmente

1. Instala las dependencias necesarias para cada microservicio:
   ```sh
   pip install -r microservicio1/requirements.txt
   pip install -r microservicio2/requirements.txt
   pip install pytest
   ```

2. Ejecuta las pruebas de cada microservicio:
   ```sh
   pytest microservicio1/tests/
   pytest microservicio2/tests/
   ```

### Ejecutar pruebas dentro del contenedor Docker

1. Asegúrate de que las carpetas `tests/` estén incluidas en el contexto de los Dockerfile y que `pytest` esté en los `requirements.txt`.
2. Levanta los contenedores:
   ```sh
   docker-compose up --build
   ```
3. Ejecuta las pruebas dentro de cada contenedor:
   ```sh
   docker exec -it <nombre_contenedor_microservicio1> pytest tests/
   docker exec -it <nombre_contenedor_microservicio2> pytest tests/
   ```
   Reemplaza `<nombre_contenedor_microservicio1>` y `<nombre_contenedor_microservicio2>` por los nombres reales de los contenedores (puedes verlos con `docker ps`).

---

Las pruebas cubren:

- **microservicio1:** Todos los endpoints de productos (creación, consulta, actualización, listado y eliminación).
- **microservicio2:** Los endpoints de precios, incluyendo la integración con el microservicio1, el cálculo de precio final, validación de país y producto, y manejo de cupones.