from .debug import router as debug_router
from .trains import router as trains_router
from .layers import router as layers_router

routers = [debug_router, trains_router, layers_router]
