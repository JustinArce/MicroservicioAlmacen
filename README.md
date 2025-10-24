# Sistema de Gestión para E-commerce

Este repositorio contiene el backend para un sistema de gestión de una tienda online, diseñado bajo una arquitectura de microservicios. El proyecto incluye la implementación del microservicio de "Catálogo de Productos" y la propuesta arquitectónica para el sistema completo.

## 1. Visión General del Proyecto

Este proyecto busca construir un sistema interno robusto para una tienda online, enfocado en dos dominios de negocio principales: la **gestión del catálogo de productos** y la **administración del ciclo de vida de los pedidos**. El sistema está diseñado para proporcionar un control total sobre las operaciones de inventario (altas, bajas, modificaciones) y para registrar un historial auditable y detallado de cada pedido, desde su creación hasta la entrega.

Además, la arquitectura está preparada para soportar futuras herramientas de analítica y business intelligence, permitiendo a la empresa tomar decisiones estratégicas basadas en datos como los productos más vendidos, tiempos promedio de entrega o la actividad de los clientes.

## 2. Arquitectura del Sistema

La solución se basa en una arquitectura de microservicios orientada a eventos, diseñada para ser escalable, resiliente y mantenible a largo plazo.

### Enfoque Arquitectónico

Se propone una arquitectura de microservicios para aislar los dominios de negocio de Pedidos y Productos. Se aplica el patrón **Event Sourcing** en el servicio de Pedidos, utilizando el historial de eventos como fuente de la verdad para garantizar la trazabilidad completa. Para optimizar las consultas y potenciar la analítica, se implementa **CQRS**, separando la escritura (eventos) de la lectura, la cual se sirve desde **Vistas Materializadas** pre-calculadas. La comunicación asíncrona vía un **Bus de Eventos** desacopla los servicios, mientras que un **API Gateway** centraliza el acceso.

### Diagrama de la Arquitectura

```mermaid
graph TD
    subgraph "Cliente"
        Client[<fontsize=4>📱<br>App Web/Móvil</font>]
=======
        Client[<font size=5>📱<br>App Web/Móvil</font>]
>>>>>>> Stashed changes
    end

    subgraph "Infraestructura Común"
        Gateway(API Gateway)
<<<<<<< Updated upstream
        EventBus{<fontsize=4>Bus de Eventos</font><br><fontsize=2>RabbitMQ / Kafka</font>}
=======
        EventBus{<font size=5>Bus de Eventos</font><br><font size=2>RabbitMQ / Kafka</font>}
>>>>>>> Stashed changes
    end

    Client -- Peticiones HTTP --> Gateway

    subgraph "Microservicio de Pedidos (CQRS / Event Sourcing)"
        direction LR
        subgraph "Lado de Escritura (Commands)"
            CmdHandler(Manejador de Comandos)
<<<<<<< Updated upstream
            EventStore[(<fontsize=4>Almacén de Eventos</font><br><fontsize=2>Fuente de la Verdad</font>)]
=======
            EventStore[(<font size=5>Almacén de Eventos</font><br><font size=2>Fuente de la Verdad</font>)]
>>>>>>> Stashed changes
        end
        
        subgraph "Lado de Lectura (Queries)"
            Projectors(Proyectores)
<<<<<<< Updated upstream
            ReadDB[(<fontsize=4>Vistas Materializadas</font><br><fontsize=2>Optimizado para Lectura</font>)]
=======
            ReadDB[(<font size=e=5>Vistas Materializadas</font><br><font size=2>Optimizado para Lectura</font>)]
>>>>>>> Stashed changes
        end
        
        CmdHandler -- Guarda Evento --> EventStore
        CmdHandler -- Publica Evento --> EventBus
        EventStore -- Flujo de Eventos --> Projectors
        Projectors -- Construye/Actualiza --> ReadDB
    end
    
    subgraph "Microservicio de Almacén (CRUD)"
        ProductAPI(API de Productos)
<<<<<<< Updated upstream
        ProductDB[(<fontsize=4>Base de Datos</font><br><fontsize=2>Catálogo de Productos</font>)]
=======
        ProductDB[(<font size=5>Base de Datos</font><br><font size=2>Catálogo de Productos</font>)]
>>>>>>> Stashed changes
        ProductAPI --- ProductDB
    end
    
    subgraph "Sistema de Analítica (BI)"
<<<<<<< Updated upstream
        Analytics[<fontsize=4>📊<br>Herramientas de Analítica</font>]
=======
        Analytics[<font size=5>📊<br>Herramientas de Analítica</font>]
>>>>>>> Stashed changes
    end

    %% --- Flujos de Datos ---
    Gateway -- 1. Comando 'CrearPedido' --> CmdHandler
    Gateway -- 2. Query 'ObtenerPedidos' --> ReadDB
    Gateway -- 3. Peticiones CRUD --> ProductAPI
    
    EventBus -- 4. Consume Evento 'PedidoConfirmado' --> ProductAPI
    
    ReadDB -- 5. Genera Informes --> Analytics
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
```

---

## 3. Microservicio de Catálogo de Productos (Implementación)

Esta sección detalla la implementación del primer componente del sistema: el microservicio de gestión del catálogo de productos.

### Descripción

Se ha implementado una API RESTful que ofrece operaciones CRUD (Crear, Leer, Actualizar, Borrar) para los productos del inventario. La API está construida con Python y FastAPI, lo que proporciona documentación interactiva automática (Swagger/OpenAPI). Todo el entorno está containerizado usando Docker y Docker Compose, incluyendo la base de datos PostgreSQL y un gateway Nginx como proxy inverso.

### Estructura de Archivos del Proyecto

Para levantar el entorno localmente, la siguiente estructura de archivos es necesaria en el directorio raíz:
- `api.py`: El código fuente de la API de productos.
- `requirements.txt`: Las dependencias de Python.
- `Dockerfile`: Las instrucciones para construir la imagen de la API.
- `docker-compose.yml`: El orquestador para todos los servicios.
- `nginx.conf`: La configuración del gateway.
- `api.env`: Variables de entorno para la API.
- `db.env`: Variables de entorno para la base de datos.

### Cómo Empezar

1.  **Requisitos Previos:** Tener Docker y Docker Compose instalados.
2.  **Configuración:** Clonar este repositorio o colocar todos los archivos en un mismo directorio.
3.  **Lanzamiento:** Abrir una terminal en el directorio del proyecto y ejecutar el siguiente comando para construir las imágenes y levantar los contenedores:
    ```bash
    docker-compose up --build
    ```
4.  **Acceso:** Una vez levantado, el sistema será accesible a través del gateway en `http://localhost:1234`.

### Endpoints de la API

<<<<<<< Updated upstream
| Método     | URL                                    | Descripción                                         |
| :-----     | :------------------------------------- | :-------------------------------------------------- |
| `GET`      | `/almacen`                             | Redirige a la documentación interactiva.            |
| `GET`      | `/almacen/docs`                        | Muestra la documentación interactiva (Swagger UI).  |
| `GET`      | `/almacen/redoc`                       | Muestra la documentación de lectura (ReDoc).        |
| `GET`      | `/almacen/productos`                   | Obtiene la lista de todos los productos.            |
| `POST`     | `/almacen/productos`                   | Crea un nuevo producto.                             |
| `GET`      | `/almacen/productos/{producto_id}`     | Obtiene un producto específico por su ID.           |
| `PUT`      | `/almacen/productos/{producto_id}`     | Actualiza un producto existente por su ID.          |
| `DELETE`   | `/almacen/productos/{producto_id}`     | Elimina un producto por su ID.                      |
=======
| Método | URL                                    | Descripción                                         |
| :----- | :------------------------------------- | :-------------------------------------------------- |
| `GET`  | `/almacen`                             | Redirige a la documentación interactiva.            |
| `GET`  | `/almacen/docs`                        | Muestra la documentación interactiva (Swagger UI).  |
| `GET`  | `/almacen/redoc`                       | Muestra la documentación de lectura (ReDoc).        |
| `GET`  | `/almacen/productos`                   | Obtiene la lista de todos los productos.            |
| `POST` | `/almacen/productos`                   | Crea un nuevo producto.                             |
| `GET`  | `/almacen/productos/{producto_id}`     | Obtiene un producto específico por su ID.           |
| `PUT`  | `/almacen/productos/{producto_id}`     | Actualiza un producto existente por su ID.          |
| `DELETE` | `/almacen/productos/{producto_id}` | Elimina un producto por su ID.                      |
>>>>>>> Stashed changes
