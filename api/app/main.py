from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, profiles, media, listings, interactions

app = FastAPI(
    title="DesignHire API",
    description="Tinder-style designer marketplace API",
    version="0.1.0",
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(media.router)
app.include_router(listings.router)
app.include_router(interactions.router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "designhire-api"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "DesignHire API",
        "version": "0.1.0",
        "docs": "/docs",
    }
