import os

from ayon_core.addon import (
    AYONAddon,
    IPluginPaths,
)

"""
from ayon_server.secrets import Secrets

# this implementation dont work because clients cant use server secret
"""


from .version import __version__

NEXTCLOUD_ROOT = os.path.dirname(os.path.abspath(__file__))



class NextCloudAddon(AYONAddon, IPluginPaths):
    """NextCloud addon class."""

    label = "NextCloud"
    name = "nextcloud"
    version = __version__

    #async this implementation dont work because clients cant use server secret
    def initialize(self, settings):
        """Initialization of addon."""

        nextcloud_settings = settings["nextcloud"]
        # Add API URL schema
        nextcloud_url = nextcloud_settings["server"].strip()

        """ this implementation dont work because clients cant use server secrets
        nextcloud_login = await Secrets.get(nextcloud_settings.login_email)
        nextcloud_password = await Secrets.get(nextcloud_settings.login_password)
        """
        nextcloud_login = nextcloud_settings["login_email"].strip()
        nextcloud_password = nextcloud_settings["login_password"].strip()
        anamoy_root = nextcloud_settings["anamoy_root"].strip()
        nextcloud_mount = nextcloud_settings["nextcloud_mount"].strip()
        publish_folder = nextcloud_settings["publish_folder"].strip()

        if nextcloud_url:
           # Ensure web url
            if not nextcloud_url.startswith("http"):
                nextcloud_url = f"https://{nextcloud_url}"


        self.server_url = nextcloud_url
        self.nextcloud_login = nextcloud_login
        self.nextcloud_password = nextcloud_password
        self.anamoy_root = anamoy_root
        self.nextcloud_mount = nextcloud_mount
        self.publish_folder = publish_folder


        # UI which must not be created at this time
        self._dialog = None
       
    def get_global_environments(self):
        """NextCloud's global environments."""
        return {"NEXTCLOUD_SERVER": self.server_url,
                "NEXTCLOUD_LOGIN": self.nextcloud_login,
                "NEXTCLOUD_PASSWORD": self.nextcloud_password,
                "AYON_ROOT": self.anamoy_root,
                "NEXTCLOUD_MOUNT": self.nextcloud_mount,
                "PUBLISH_FOLDER": self.publish_folder}

    def get_plugin_paths(self):
        """Implementation of abstract method for `IPluginPaths`."""

        return {
            "publish": self.get_publish_plugin_paths(),
            # The laucher action is not working since AYON conversion
            # "actions": [os.path.join(NEXTCLOUD_ROOT, "plugins", "launcher")],
        }

    def get_publish_plugin_paths(self, host_name=None):
        return [os.path.join(NEXTCLOUD_ROOT, "plugins", "publish")]

def is_nextcloud_enabled_in_settings(project_settings):
    nextcloud_enabled = project_settings.get("enabled")
    # If 'nextcloud_enabled' is not set, we assume it is enabled.
    # - this is for backwards compatibility - remove in future
    if nextcloud_enabled is None:
        return True
    return nextcloud_enabled