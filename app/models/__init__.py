# Import all the models, so that Base has them before being


# imported by Alembic
from app.models.model_user import User
document_models = [
    User
]
