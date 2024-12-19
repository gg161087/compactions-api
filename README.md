# Sistema de Generación de Actas de Compactación

Este sistema permite la generación y gestión de actas de compactación de vehículos de manera eficiente y organizada. El sistema está compuesto por un backend desarrollado con FastAPI y un frontend con React, y se despliega en contenedores Docker para simplificar su configuración y ejecución.

## Propósito

El propósito de este sistema es digitalizar y optimizar el proceso de creación y administración de actas de compactación, facilitando el registro y consulta de información relevante como los vehículos involucrados, testigos, responsables y ubicaciones. 

## Estructura del Proyecto

- **Backend**: 
  - Implementado con **FastAPI**.
  - Administra la lógica de negocio, maneja la comunicación con la base de datos y expone una API para la interacción con el frontend.
  - Incluye endpoints para la creación, edición y consulta de actas de compactación.
  
- **Frontend**:
  - Desarrollado con **React**.
  - Proporciona una interfaz de usuario intuitiva para la gestión de las actas, facilitando la creación y visualización de datos.
  
- **Base de Datos**:
  - Utiliza **MySQL** como motor de base de datos para almacenar los datos de las actas, personas, depósitos y vehículos asociados.

## Requisitos

- **Docker** y **Docker Compose** instalados en el sistema.

## Configuración y Ejecución

1. **Clonar el repositorio**:
   ```bash   
   git clone https://gitlab.slyt.gba.gov.ar/juan.pascual/proyecto-compactaciones
   cd proyecto-compactaciones
   docker compose up
  crear .env
    SECRET_KEY=ThisIsNotSecret
    ALGORITHM=HS256
    DATABASE_URL=mysql+pymysql://user:pwd@ip:3306/db_name  