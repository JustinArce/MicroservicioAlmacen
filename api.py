import os
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, select, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# --- Configuración ---
class DBSettings(BaseSettings):
    database_url: str = "postgresql+psycopg2://user:password@db:5432/almacen_db"

db_settings = DBSettings()

# --- Conexión a la Base de Datos ---
db_engine = create_engine(db_settings.database_url) # echo=True es útil para depurar, pero puede ser ruidoso

class BaseEntity(DeclarativeBase):
    pass

class Producto(BaseEntity):
    __tablename__ = "productos"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(350), nullable=False)
    precio: Mapped[float] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)
    categoria: Mapped[Optional[str]] = mapped_column(String(50))

# --- Modelos Pydantic Mejorados ---
class ProductoBase(BaseModel):
    # AÑADIDO: Se usa Field para añadir metadatos a la documentación
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del producto.", example="Monitor Curvo 27 pulgadas")
    descripcion: str = Field(..., min_length=1, max_length=350, description="Descripción detallada del producto.", example="Monitor gaming con resolución 4K y 144Hz de tasa de refresco.")
    precio: float = Field(..., gt=0.0, description="Precio de venta del producto. Debe ser mayor que cero.", example=399.99)
    stock: int = Field(..., ge=0, description="Cantidad de unidades disponibles en el inventario.", example=75)
    categoria: Optional[str] = Field(None, description="Categoría a la que pertenece el producto.", example="Electrónica")

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    # Permite actualizaciones parciales
    nombre: Optional[str] = Field(None, min_length=1, max_length=100, description="Nuevo nombre del producto.", example="Monitor Curvo 27\" Gen 2")
    descripcion: Optional[str] = Field(None, min_length=1, max_length=350, description="Nueva descripción detallada.")
    precio: Optional[float] = Field(None, gt=0.0, description="Nuevo precio de venta.", example=379.99)
    stock: Optional[int] = Field(None, ge=0, description="Nueva cantidad en stock.", example=60)
    categoria: Optional[str] = Field(None, description="Nueva categoría del producto.", example="Monitores")


class ProductoResponse(ProductoBase):
    id: int = Field(description="Identificador único del producto generado por el sistema.", example=1)
    class Config:
        from_attributes = True

class ListaProductosResponse(BaseModel):
    productos: List[ProductoResponse]

# --- Ciclo de vida de la aplicación ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    BaseEntity.metadata.create_all(bind=db_engine)
    yield

# --- Instancia de la App FastAPI Mejorada ---
root_path = os.getenv("ROOT_PATH", "")

# AÑADIDO: Metadatos para la documentación
app = FastAPI(
    title="API de Almacén",
    description="API RESTful para gestionar el catálogo de productos de una tienda online. Permite realizar operaciones CRUD completas.",
    version="1.0.0",
    lifespan=lifespan,
    root_path=root_path,
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- Dependencia para la Sesión de la Base de Datos ---
def get_db_session():
    with Session(db_engine) as session:
        yield session

# --- Endpoints de la API con Documentación ---
@app.get("/", include_in_schema=False)
def redirect_to_docs():
    """
    Redirige la ruta raíz a la documentación interactiva de la API.
    """
    return RedirectResponse(url=f"{root_path}/docs")

@app.post("/productos", response_model=ProductoResponse, status_code=201, tags=["Productos"])
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db_session)):
    """
    Crea un nuevo producto en el inventario.

    - Recibe los datos de un producto en el cuerpo de la petición.
    - Almacena el nuevo producto en la base de datos.
    - Devuelve el producto recién creado con su ID asignado.
    """
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.get("/productos", response_model=ListaProductosResponse, tags=["Productos"])
def obtener_productos(db: Session = Depends(get_db_session)):
    """
    Obtiene una lista de todos los productos disponibles en el almacén.
    """
    productos_db = db.scalars(select(Producto).order_by(Producto.id)).all()
    return {"productos": productos_db}

@app.get("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
def obtener_producto(producto_id: int, db: Session = Depends(get_db_session)):
    """
    Obtiene la información de un producto específico por su ID.
    """
    producto_db = db.get(Producto, producto_id)
    if producto_db is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto_db

@app.put("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
def actualizar_producto(producto_id: int, producto_update: ProductoUpdate, db: Session = Depends(get_db_session)):
    """
    Actualiza la información de un producto existente.

    - Permite actualizaciones parciales: solo se modifican los campos incluidos en la petición.
    """
    db_producto = db.get(Producto, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    update_data = producto_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_producto, key, value)
    
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.delete("/productos/{producto_id}", status_code=204, tags=["Productos"])
def eliminar_producto(producto_id: int, db: Session = Depends(get_db_session)):
    """
    Elimina un producto del inventario por su ID.
    """
    db_producto = db.get(Producto, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()
    return None