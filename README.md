# CRUD-PYTHON-POSTGRES

# API de Películas

Este proyecto es una API para administrar información sobre películas. Permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre una base de datos de películas utilizando FastAPI y PostgreSQL.

## Tecnologías utilizadas

- **FastAPI**: Un marco web moderno y rápido para Python.
- **PostgreSQL**: Un sistema de gestión de bases de datos relacional de código abierto y potente.

## Endpoints

- `GET /films`: Obtiene todas las películas.
- `GET /films/{id}`: Obtiene una película por su ID.
- `POST /films/`: Crea una nueva película.
- `PUT /films/{id}`: Actualiza una película existente por su ID.
- `DELETE /films/{id}`: Elimina una película por su ID.

## Objetivos

1. **Aprender a utilizar FastAPI**:
   - Aprender a definir rutas y manejar solicitudes HTTP utilizando FastAPI.
   - Entender cómo validar datos de entrada y salida utilizando Pydantic.

2. **Aprender a hacer consultas con PostgreSQL**:
   - Familiarizarse con la sintaxis de consulta de PostgreSQL.
   - Aprender a utilizar el controlador psycopg2 para interactuar con PostgreSQL desde Python.

3. **CRUD Python**:
   - Implementar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) utilizando Python y PostgreSQL.
   - Comprender cómo estructurar y organizar el código para realizar operaciones de base de datos de manera eficiente y segura.

4. **Consultas con parámetros de consulta**:
   - Aprender a manejar parámetros de consulta en las solicitudes HTTP.
   - Implementar consultas personalizadas utilizando parámetros de consulta para filtrar y ordenar datos.
