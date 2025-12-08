from .admin.callback import router as admin_callback
from .admin.command import router as admin_command
from .admin.message import router as admin_message
from .intercept.intercept import get_router_intercept
from .user.callback import get_router_user_callback
from .user.command import get_router_user_command
from .user.message import get_router_user_message
from .user.payment import get_router_user_payment

__all__: list[str] = [
    "admin_callback",
    "admin_command",
    "admin_message",
    "get_router_intercept",
    "get_router_user_callback",
    "get_router_user_command",
    "get_router_user_message",
    "get_router_user_payment",
]
