from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    APP_NAME: str = "EL CLIENTE - Fondos API"
    API_V1_PREFIX: str = "/api/v1"
    AWS_REGION: str = os.environ.get("AWS_REGION", "us-east-1")
    
    # Nombres de tablas DynamoDB
    CLIENTS_TABLE_NAME: str = os.environ.get("CLIENTS_TABLE_NAME", "Clients")
    FUNDS_TABLE_NAME: str = os.environ.get("FUNDS_TABLE_NAME", "Funds")
    SUBSCRIPTIONS_TABLE_NAME: str = os.environ.get("SUBSCRIPTIONS_TABLE_NAME", "Subscriptions")
    TRANSACTIONS_TABLE_NAME: str = os.environ.get("TRANSACTIONS_TABLE_NAME", "Transactions")
    
    # Valores default para desarrollo local
    DEFAULT_CLIENT_ID: str = os.environ.get("DEFAULT_CLIENT_ID", "C123456")
    
    class Config:
        env_file = ".env"

settings = Settings()