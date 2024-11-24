from app.core.config import settings
from app.models import document_models

import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of document models
async def startDB():
    while True:
        try:
            # Create Motor client
            client = AsyncIOMotorClient(settings.DB_URL)
            print(settings.DB_URL)
            # Init beanie with the list of document models
            await init_beanie(database=client.db_name, document_models=document_models)

            logger.info('Database connected successfully')
            return client
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            logger.info("Retrying connection in 5 seconds...")
            await asyncio.sleep(5)  # Wait for 5 seconds before trying again
