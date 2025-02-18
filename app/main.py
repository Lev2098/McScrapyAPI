from fastapi import FastAPI

from app.routers.product import router

app = FastAPI(
    title="McScraperAPI",
    description="Scrape and api",
    docs_url="/docs",
    redoc_url="/redoc"
)

api_version_prefix = "/api/v1"

app.include_router(router=router, prefix=f"{api_version_prefix}/products", tags=["products"])

