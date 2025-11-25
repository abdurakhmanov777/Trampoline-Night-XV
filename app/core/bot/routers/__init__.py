from app.core.bot.routers.admin.callback import router as admin_callback
from app.core.bot.routers.admin.command import router as admin_command
from app.core.bot.routers.admin.message import router as admin_message
from app.core.bot.routers.intercept.intercept import router as intercept
from app.core.bot.routers.user.callback import router as user_callback
from app.core.bot.routers.user.command import router as user_command
from app.core.bot.routers.user.message import router as user_message

__all__: list[str] = [
    "admin_callback",
    "admin_command",
    "admin_message",
    "intercept",
    "user_callback",
    "user_command",
    "user_message",
]
