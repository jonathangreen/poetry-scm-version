from typing import Optional

from poetry.console.application import Application

from .base_plugin import BasePlugin as BasePlugin

class ApplicationPlugin(BasePlugin):
    type: str
    def activate(self, application: Optional[Application]) -> None: ...
