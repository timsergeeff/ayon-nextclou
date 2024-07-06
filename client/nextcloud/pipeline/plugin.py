import pyblish.api
from ayon_core.pipeline.publish import (
    get_plugin_settings,
    apply_plugin_settings_automatically,
)
from nextcloud.addon import is_nextcloud_enabled_in_settings

SETTINGS_CATEGORY = "nextcloud"


class NextCloudPublishContextPlugin(pyblish.api.ContextPlugin):
    settings_category = SETTINGS_CATEGORY
    _original_enabled = None

    @classmethod
    def is_nextcloud_enabled(cls, project_settings):
        return is_nextcloud_enabled_in_settings(
            project_settings.get(SETTINGS_CATEGORY) or {}
        )

    @classmethod
    def apply_settings(cls, project_settings):
        if cls._original_enabled is None:
            cls._original_enabled = getattr(cls, "enabled", True)

        if not cls.is_nextcloud_enabled(project_settings):
            cls.enabled = False
            return

        cls.enabled = cls._original_enabled

        plugin_settins = get_plugin_settings(
            cls, project_settings, cls.log, None
        )
        apply_plugin_settings_automatically(cls, plugin_settins, cls.log)


class NextCloudPublishInstancePlugin(pyblish.api.InstancePlugin):
    settings_category = SETTINGS_CATEGORY
    _original_enabled = None

    @classmethod
    def is_nextcloud_enabled(cls, project_settings):
        return is_nextcloud_enabled_in_settings(
            project_settings.get(SETTINGS_CATEGORY) or {}
        )

    @classmethod
    def apply_settings(cls, project_settings):
        if cls._original_enabled is None:
            cls._original_enabled = getattr(cls, "enabled", True)

        if not cls.is_nextcloud_enabled(project_settings):
            cls.enabled = False
            return

        cls.enabled = cls._original_enabled

        plugin_settins = get_plugin_settings(
            cls, project_settings, cls.log, None
        )
        apply_plugin_settings_automatically(cls, plugin_settins, cls.log)
