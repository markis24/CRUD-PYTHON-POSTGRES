import json
from datetime import datetime

from fastapi import HTTPException

from db import database
from model.product import ProductCreate


def read():
    try:
        # Conexión a la base de datos
        conn = database.client()
        cursor = conn.cursor()

        # Ejecutar la consulta SQL
        query = "SELECT * FROM product"
        cursor.execute(query)

        # Obtener los resultados
        result = cursor.fetchall()

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {e}")


def read_product_by_id(product_id: int):
    try:
        # Conexión a la base de datos
        conn = database.client()
        cursor = conn.cursor()

        # Ejecutar la consulta SQL
        query = "SELECT * FROM product WHERE product_id=%s"
        cursor.execute(query, (product_id,))

        # Obtener el resultado
        result = cursor.fetchone()

        # Verificar si se encontró el producto
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")


def create_product(product: ProductCreate):
    try:
        # Conexión a la base de datos
        conn = database.client()
        cursor = conn.cursor()

        # Obtener la fecha y hora actual
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Ejecutar la inserción
        cursor.execute("""
                INSERT INTO product (name, description, company, price, units, subcategory_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            product.name, product.description, product.company, product.price, product.units,
            product.subcategory_id,
            current_time, current_time))

        conn.commit()

        return "Registro añadido exitosamente"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {e}")


def update_products(product_id: int, product: ProductCreate):
    try:
        # Conexión a la base de datos
        conn = database.client()
        cursor = conn.cursor()

        # Obtener la fecha y hora actual
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Ejecutar la actualización
        cursor.execute(
            "UPDATE product SET name = %s, description = %s, company = %s, price = %s, units = %s, "
            "subcategory_id = %s, created_at = %s, updated_at = %s WHERE product_id = %s",
            (
                product.name, product.description, product.company, product.price, product.units,
                product.subcategory_id, current_time, current_time, product_id
            )
        )

        conn.commit()

        return "Registro actualizado exitosamente"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {e}")


def delete_by_id(product_id: int):
    try:
        # Conexión a la base de datos
        conn = database.client()
        cursor = conn.cursor()

        # Ejecutar la consulta SQL
        query = "DELETE FROM product WHERE product_id=%s"
        cursor.execute(query, (product_id,))
        conn.commit()

        # Verificar si se eliminó algún producto
        if cursor.rowcount > 0:
            return {"message": "Producto eliminado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")


def all_products():
    try:
        # Conexión a la base de datos
        conn = database.client()
        cursor = conn.cursor()

        # Ejecutar la consulta SQL
        query = """
            SELECT c.name AS category_name,
                   s.name AS subcategory_name,
                   p.name AS product_name,
                   p.company,
                   p.price
            FROM product p
            JOIN subcategory s ON p.subcategory_id = s.subcategory_id
            JOIN category c ON s.category_id = c.category_id;
        """
        cursor.execute(query)

        # Obtener los resultados
        products = cursor.fetchall()

        # Formatear los resultados en un diccionario por producto
        formatted_products = []
        for product in products:
            # Convertir el precio de Decimal a float
            price = float(product[4])

            formatted_product = {
                "category_name": product[0],
                "subcategory_name": product[1],
                "product_name": product[2],
                "company": product[3],
                "price": price  # Usar el precio convertido a float
            }
            formatted_products.append(formatted_product)

        # Convertir la lista de diccionarios a una cadena JSON utilizando json.dumps
        json_products = json.dumps(formatted_products)

        return json_products

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {e}")


def load_products(file_content: bytes) -> Dict[str, str]:
    try:
        # Crear un objeto BytesIO a partir del contenido del archivo
        file_object = BytesIO(file_content)

        # Leer el archivo CSV directamente desde el objeto BytesIO
        import pandas as pd
        df = pd.read_csv(file_object)

        # Verificar si las columnas necesarias existen en el DataFrame
        required_columns = ['nom_categoria', 'nom_subcategoria', 'nom_producto']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"La columna '{col}' no está presente en el archivo CSV.")

        # Conexión a la base de datos
        conn = database.client()
        cursor = conn.cursor()

        # Obtener la fecha y hora actual
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Iterar sobre cada fila del DataFrame
        for index, row in df.iterrows():
            category_name = row['nom_categoria']
            subcategory_name = row['nom_subcategoria']
            product_name = row['nom_producto']

            # Insertar o actualizar categoría
            cursor.execute("SELECT category_id FROM category WHERE name = %s", (category_name,))
            category_id = cursor.fetchone()
            if category_id:
                cursor.execute("UPDATE category SET updated_at = %s WHERE category_id = %s",
                               (current_time, category_id[0]))
            else:
                cursor.execute("INSERT INTO category (name, created_at, updated_at) VALUES (%s, %s, %s)",
                               (category_name, current_time, current_time))
                conn.commit()  # Guardar cambios para obtener el ID generado automáticamente
                category_id = cursor.lastrowid

            # Insertar o actualizar subcategoría
            cursor.execute("SELECT subcategory_id FROM subcategory WHERE name = %s", (subcategory_name,))
            subcategory_id = cursor.fetchone()
            if subcategory_id:
                cursor.execute("UPDATE subcategory SET updated_at = %s WHERE subcategory_id = %s",
                               (current_time, subcategory_id[0]))
            else:
                cursor.execute(
                    "INSERT INTO subcategory (name, category_id, created_at, updated_at) VALUES (%s, %s, %s, %s)",
                    (subcategory_name, category_id, current_time, current_time))
                conn.commit()  # Guardar cambios para obtener el ID generado automáticamente
                subcategory_id = cursor.lastrowid

            # Insertar o actualizar producto
            cursor.execute("SELECT product_id FROM product WHERE name = %s", (product_name,))
            product_id = cursor.fetchone()
            if product_id:
                cursor.execute("UPDATE product SET updated_at = %s WHERE product_id = %s",
                               (current_time, product_id[0]))
            else:
                cursor.execute(
                    "INSERT INTO product (name, subcategory_id, created_at, updated_at) VALUES (%s, %s, %s, %s)",
                    (product_name, subcategory_id[0], current_time, current_time))

        # Confirmar la transacción y cerrar la conexión
        conn.commit()
        conn.close()

        # Devolver respuesta exitosa
        return {"message": "El proceso se ha realizado correctamente."}

    except Exception as e:
        # En caso de error, levantar una excepción HTTP
        raise HTTPException(status_code=500, detail=f"Error al cargar productos desde el archivo CSV: {e}")
