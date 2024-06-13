from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import User, Business, user_pydantic, user_pydanticIN, business_pydantic
from authentification import get_password_hash
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient

app = FastAPI()

# Fonction de signal post_save
@post_save(User)
async def create_business(
    sender: Type[User],
    instance: User,
    created: bool,
    using_db: Optional[BaseDBAsyncClient],
    update_fields: List[str]
) -> None:
    if created:
        business_obj = await Business.create(
            business_name=instance.username, owner=instance
        )
        await business_pydantic.from_tortoise_orm(business_obj)
        # Envoyer un email (à implémenter)
        # send_email()

# Point de terminaison pour l'inscription des utilisateurs
@app.post("/registration")
async def user_registration(user: user_pydanticIN):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_password_hash(user_info['password'])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return {
        "status": "ok",
        "data": f"Hello {new_user.username}, thanks for choosing our services. Please check your email inbox and click on the link to confirm your registration."
    }

@app.get("/")
def index():
    return {"message": "Hello World"}

# Enregistrement de Tortoise ORM avec FastAPI
register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)
