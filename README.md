# Proyecto Fondos de Inversión - El Cliente

Este repositorio contiene la solución implementada para la prueba técnica de Amaris Consulting - "El Cliente", una plataforma para gestionar fondos de inversión (FPV y FIC).

## Descripción del Proyecto y Reglas de Negocio

El proyecto cumple al 100% con todos los requerimientos.

## Tecnologías Utilizadas

### Versiones
- **Python**: 3.11.9
- **Node.js**: v20.13.1
- **NPM**: 10.5.2
- **AWS CLI**: 2.17.35

## Estructura del Repositorio

### `/backend`
Aplicación backend construida con:
- **FastAPI**: Framework web de Python de alto rendimiento
- **Pydantic**: Validación de datos y configuración
- **Boto3**: SDK de AWS para Python
- **DynamoDB**: Base de datos NoSQL de AWS

### `/frontend`
Aplicación frontend construida con:
- **React 19**: Biblioteca JavaScript para interfaces de usuario
- **Redux Toolkit**: Manejo del estado de la aplicación
- **Material UI**: Componentes de UI con diseño Material Design
- **Axios**: Cliente HTTP para comunicación con la API

### `/cloudformation`
Templates y scripts para despliegue automatizado en AWS:
- **template.yaml**: Template principal para infraestructura AWS
- **deploy.ps1**: Script PowerShell para automatizar el despliegue
- **backend-build-fixed.ps1**: Script para empaquetar el backend
- **frontend-build.ps1**: Script para construir el frontend

### `/database`
Scripts SQL para la segunda parte de la prueba técnica.

## Arquitectura en AWS

La solución está desplegada en AWS utilizando los siguientes servicios:
- **API Gateway**: Para exponer la API REST
- **Lambda**: Para ejecutar el código backend
- **DynamoDB**: Para almacenamiento de datos
- **S3**: Para alojar el frontend
- **CloudFront**: Para distribución del frontend
- **IAM**: Para gestión de permisos

## Despliegue

El despliegue se realizó utilizando CloudFormation para crear la infraestructura necesaria:

1. Se creó un bucket S3 para almacenar los artefactos de despliegue
2. Se empaquetó el backend y se incluyó una Layer con las dependencias requeridas
3. Se construyó el frontend y se ajustó para apuntar a la API correcta
4. Se desplegó el stack completo mediante el script `deploy.ps1`
5. Se subió el frontend al bucket S3 correspondiente
6. Se configuró CloudFront para distribución global del frontend

## URLs

- **API**: [https://85icyuszth.execute-api.us-east-1.amazonaws.com/prod](https://85icyuszth.execute-api.us-east-1.amazonaws.com/prod)
- **Aplicación Web**: [https://d9rsztvtxxjwr.cloudfront.net](https://d9rsztvtxxjwr.cloudfront.net)

## Acceso AWS para Revisión

Se ha creado un usuario IAM con permisos de solo lectura para revisión del proyecto:

- **URL de inicio de sesión**: [https://891377403177.signin.aws.amazon.com/console](https://891377403177.signin.aws.amazon.com/console)
- **Usuario**: ElClienteInterviewer
- **Contraseña**: ElClienteInterviewer1

### Recursos a revisar:

1. **DynamoDB** (tablas con prefijo "ElCliente-")  
   [https://us-east-1.console.aws.amazon.com/dynamodbv2/home?region=us-east-1#tables](https://us-east-1.console.aws.amazon.com/dynamodbv2/home?region=us-east-1#tables)

2. **Lambda** (función "ElCliente-Backend-prod")  
   [https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions](https://us-east-1.console.aws.amazon.com/lambda/home?region=us-east-1#/functions)

3. **API Gateway** (API "ElCliente-API-prod")  
   [https://us-east-1.console.aws.amazon.com/apigateway/main/apis?region=us-east-1](https://us-east-1.console.aws.amazon.com/apigateway/main/apis?region=us-east-1)

4. **S3** (buckets con prefijo "elcliente-")  
   [https://s3.console.aws.amazon.com/s3/buckets?region=us-east-1](https://s3.console.aws.amazon.com/s3/buckets?region=us-east-1)

5. **CloudFormation** (stack "ElCliente-Stack")  
   [https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks](https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks)

> **Nota**: La cuenta de usuario tiene permisos de solo lectura y expirará después de la entrevista.
