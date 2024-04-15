from fastapi import FastAPI, HTTPException, UploadFile, File

from db import productDB
from model.product import ProductCreate

app = FastAPI()


# Entrar en docs http://127.0.0.1:8000/docs

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/products")
def get_products():
    data = productDB.read()
    if not data:
        raise HTTPException(status_code=404, detail="No se encontraron productos en la base de datos")
    return {"data": data}


@app.get("/products/{id}")
def get_product_by_id(product_id: int):
    data = productDB.read_product_by_id(product_id)
    if data:
        return {"data": data}
    else:
        raise HTTPException(status_code=404, detail="No se han encontrado productos con este ID.")


@app.post("/products")
def create_product(product: ProductCreate):
    data = productDB.create_product(product)
    if data:
        return {"message": "Producto creado exitosamente"}
    else:
        raise HTTPException(status_code=500, detail="Error interno del servidor al crear el producto")


@app.put("/products/{id}")
def update_product(product_id: int, product: ProductCreate):
    data = productDB.update_products(product_id, product)
    if data:
        return {"message": "Producto actualizado exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el producto. Revise los datos enviados.")


@app.delete("/products/{id}")
def delete_product_by_id(product_id: int):
    data = productDB.delete_by_id(product_id)
    if data:
        return {"message": "Producto eliminado exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="No se pudo eliminar el producto. Verifique el ID proporcionado.")


@app.get("/productsAll")
def get_all_products():
    data = productDB.all_products()
    if not data:
        raise HTTPException(status_code=404, detail="No se encontraron productos en la base de datos")
    return {"data": data}


@app.post("/loadProducts")
async def load_products_endpoint(file: UploadFile = File(...)):
    try:
        # Verificar que el archivo sea un archivo CSV
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="El archivo debe ser un archivo CSV.")

        # Leer el contenido del archivo
        file_content = await file.read()

        # Llamar a la función para cargar productos con el contenido del archivo
        await productDB.load_products(file_content)

        return {"message": "El proceso de carga de productos se ha completado correctamente."}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {e}")
