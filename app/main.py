from fastapi import FastAPI
from app.routes.auth_routes import router
from app.routes.classifiacation_routes import class_router

def main() -> FastAPI:
    app = FastAPI(
                title='API for classification'
                )
    # app.include_router(api_router)

    return app

app = main()
app.include_router(router)
app.include_router(class_router)