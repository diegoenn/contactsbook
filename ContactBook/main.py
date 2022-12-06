from fastapi import FastAPI

from ContactBook.routers import user_create, manage_contacts

routers = (
    user_create.router,
    manage_contacts.router,
)

app = FastAPI()

for router in routers:
    app.include_router(router)
