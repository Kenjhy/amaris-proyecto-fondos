# amaris_el_cliente_backend
amaris_el_cliente_backend

# Configuración del proyecto
## Crear entorno virtual and install packages
    python -m venv venv
    venv\Scripts\activate

    pip freeze > requirements.txt

    pip install -r requirements.txt

    pip install fastapi uvicorn pydantic boto3 pytest pytest-asyncio python-jose email-validator python-dotenv httpx
    pip install pydantic-settings


# Versions

    Python version Python 3.11.9

    node -v
    v20.13.1

    npm -v
    10.5.2

    AWS CLI:
    aws --version
    aws-cli/2.17.35 Python/3.11.9 Windows/10 exe/AMD64


# Repositories Git Hub
## Repository backend
    https://github.com/Kenjhy/amaris_el_cliente_backend

## Repository Frontend
    https://github.com/Kenjhy/amaris_el_cliente_front

# Create estructure
 mkdir -p app/models 
 mkdir -p app/api/endpoints
 mkdir -p app/services
 mkdir -p test 
 mkdir -p infrastructure  

 ## Crear la estructura principal
mkdir proyecto-fondos
cd proyecto-fondos
mkdir backend
mkdir frontend
mkdir infrastructure

## Crear la estructura del backend
cd backend
mkdir app
cd app
mkdir models
mkdir services
mkdir api
cd api
mkdir endpoints
cd ..\..\
mkdir tests


# Configure dinamo bd local
##  Configurar DynamoDB local para desarrollo
    Si tienes Docker instalado en Windows, puedes usar:
    powershellCopiar# Instalar DynamoDB local via Docker
    docker pull amazon/dynamodb-local
    docker run -p 8000:8000 amazon/dynamodb-local
    Alternativamente, puedes descargar DynamoDB local directamente:

    Crea un directorio para DynamoDB local
    Descarga el archivo ZIP desde https://s3.us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.zip
    Extrae el contenido del archivo ZIP en el directorio creado
    Ejecuta DynamoDB local con Java:

    powershellCopiarcd dynamodb-local
    java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

# Execute and create scripts data base
## OJO DELETE ALL TABLES UN DATABASE
     python scripts/create_tables.py 

# Execute server backend
## Navegar al directorio raíz del backend si no estás ahí
cd proyecto-fondos\backend

## Iniciar el servidor FastAPI con Uvicorn
    uvicorn app.main:app --reload --port 8001
    http://127.0.0.1:8001/


# Deployment

proyecto-fondos/
├── cloudformation/
│   ├── template.yaml        # Plantilla principal CloudFormation
│   ├── backend-build.sh     # Script para empaquetar backend
│   └── frontend-build.sh    # Script para empaquetar frontend
├── backend/                 # código backend
├── frontend/                # código frontend
└── README.md                # Documentación