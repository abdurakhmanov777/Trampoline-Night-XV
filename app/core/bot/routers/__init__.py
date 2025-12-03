from app.core.bot.routers.admin.callback import router as admin_callback
from app.core.bot.routers.admin.command import router as admin_command
from app.core.bot.routers.admin.message import router as admin_message
from app.core.bot.routers.intercept.intercept import intercept_handler
from app.core.bot.routers.user.callback import user_callback
from app.core.bot.routers.user.command import user_command
from app.core.bot.routers.user.message import user_message

__all__: list[str] = [
    "admin_callback",
    "admin_command",
    "admin_message",
    "intercept_handler",
    "user_callback",
    "user_command",
    "user_message",
]
