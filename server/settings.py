from ayon_server.settings import BaseSettingsModel, SettingsField
from ayon_server.settings.enum import secrets_enum

__all__ = (
    "DEFAULT_VALUES",
    "NextCloudSettings",
)

class BasicEnabledStatesModel(BaseSettingsModel):
    enabled: bool = SettingsField(True, title="Enabled")
    optional: bool = SettingsField(True, title="Optional")
    active: bool = SettingsField(True, title="Active")

class PublishPluginsModel(BaseSettingsModel):
    IntegrateNextcloudShare: BasicEnabledStatesModel= SettingsField(
        default_factory=BasicEnabledStatesModel,
        title="NextCloud share"
    )

class NextCloudSettings(BaseSettingsModel):
    enabled: bool = SettingsField(True, title="Enabled")
    server: str = SettingsField(
        "",
        title="NextCloud Server",
        scope=["studio"],
    )
    login_email: str = SettingsField(
        "",
        title="NextCloud LOGIN",
        scope=["studio"],
    )
    login_password: str = SettingsField(
        "",
        title="NextCloud user password",
        scope=["studio"],
    )
    """ this logic is not working for publicher because clients cant use server secrets
    login_email: str = SettingsField(
        "nextcloud_email",
        enum_resolver=secrets_enum,
        title="NextCloud user email",
        scope=["studio"],
    )
    login_password: str | None = SettingsField(
        "nextcloud_password",
        enum_resolver=secrets_enum,
        title="NextCloud user password",
        scope=["studio"],
    )
    """
    anamoy_root: str = SettingsField(
        "",
        title="Ayon Anatomy root",
        scope=["studio"],
    )
    nextcloud_mount: str = SettingsField(
        "",
        title="NextCloud mount replasing Anatomy root",
        scope=["studio"],
    )
    publish_folder: str = SettingsField(
        "",
        title="Publish_folder",
        scope=["studio"],
    )

    publish: PublishPluginsModel = SettingsField(
        default_factory=PublishPluginsModel,
        title="Publish"
    )

DEFAULT_VALUES = {}