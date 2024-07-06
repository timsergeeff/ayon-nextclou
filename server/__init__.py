from typing import Type

from nxtools import logging

from ayon_server.addons import BaseServerAddon
from ayon_server.api.responses import EmptyResponse
from ayon_server.exceptions import ForbiddenException, InvalidSettingsException
from ayon_server.secrets import Secrets

from .settings import NextCloudSettings, DEFAULT_VALUES

class NextCloudAddon(BaseServerAddon):
    settings_model: Type[NextCloudSettings] = NextCloudSettings  