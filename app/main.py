from fastapi import FastAPI

from app.routers import product

app = FastAPI(
    title="McScraperAPI",
    description="Scrape and api",
)

api_version_prefix = "/api/v1"

app.include_router(
    product.router, prefix=f"{api_version_prefix}/products", tags=["products"]
)
