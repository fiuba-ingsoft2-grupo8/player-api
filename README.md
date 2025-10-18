# Player API

## Requisitos

- Docker y Docker Compose.
- Python 3.9+ (para desarrollo local y testing).

## Ejecución del Proyecto con Make

Este proyecto incluye un Makefile con varios comandos diseñados para simplificar las tareas de desarrollo y despliegue.

### Comandos disponibles 

#### Construir la Imagen de Docker

```bash
make build-system
```

Construye la imagen de Docker para el servicio player-api con la etiqueta player-api:latest.

#### Iniciar la Aplicación

```bash
make up
```

Construye la imagen de Docker (si aún no está construida) y levanta todos los servicios definidos en docker-compose.yml en modo desacoplado.

**Este comando:**
- Construye el sistema si es necesario
- Inicia los contenedores en segundo plano
- Elimina los contenedores huérfanos

#### Detener la Aplicación

```bash
make down
```

Detiene y elimina todos los contenedores definidos en docker-compose.yml.

#### Ejecutar las Pruebas

```bash
make test
```

Ejecuta el conjunto de pruebas utilizando pytest con un reporte de cobertura de código.

El informe de cobertura se genera en formato XML (coverage.xml).

### Inicio Rápido

1. **Configuración inicial:** Construir e iniciar la aplicación.
   ```bash
   make up
   ```

2. **Ejecutar pruebas:** Correr la suite de tests.
   ```bash
   make test
   ```

3. **Detener la aplicación:** Cuando hayas terminado.
   ```bash
   make down
   ```
