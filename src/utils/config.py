import shutil
import os
import json
from platformdirs import user_config_dir

# A class for accessing base configurations such as the default safe path and removing the app folders.
#   This class exists as a lightweight alternative to AppConfig class when only minimal configuration is needed.
#   This class allows you to:
#       - Get the default safe file path
#       - Delete app config folders/file
class SafeConfig():
    def __init__(self):
        app_name = "SuperDuperSecret"
        app_author = "SuperDuperSecret"

        self.config_dir = user_config_dir(app_name, app_author)

        # Ensure config directories exist
        os.makedirs(self.config_dir, exist_ok=True)
        
        self.default_safe_path = os.path.join(self.config_dir, "default-safe.json")

    def get_default_safe_path(self):
        return self.default_safe_path

    def delete_all(self):
        print(f"[WARNING] This will delete everything within '{self.config_dir}'")
        authorize = input("Proceed? (y/N) > ")

        if authorize.lower() == "y":
            try:
                if os.path.exists(self.config_dir):
                    shutil.rmtree(self.config_dir)
                    print(f"[INFO] Deleted: {self.config_dir}")
                else:
                    print("[INFO] Did not delete config as it does not exist.")
            except Exception as e:
                print(f"[ERROR] Could not delete: {self.config_dir}")
        else:
            print("operation canceled")

# AppConfig extends the functionality of SafeConfig to include more config features.
#   A general class that can be used for all program configuration options.
#   This class allows you to:
#       - Get the default safe file path
#       - Delete app config folders/file
#       - Add custom config entries
class AppConfig(SafeConfig):
    def __init__(self):
        super().__init__()
        self.data = {}

        self.config_path = os.path.join(self.config_dir, "settings.json")
        # Attempt to load config
        self._load_config()

    def _save_config(self) -> None:
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.data, f)
            print(f"[INFO] Config saved to: {self.config_path}")
        except Exception as e:
            print(f"[ERROR] Could not load config from: {self.config_path}")

    # Returns an empty dictionary if config file does not exist
    # Returns the config as a dictionary if the config file exists
    def _load_config(self) -> None:
        if not os.path.exists(self.config_path):
            self.data = {}
        else:
            with open(self.config_path, "r") as f:
                self.data = json.load(f)

    # Add an entry or update an existing entry. This automatically updates the config file
    def add_or_update_entry(self, key: str, value: str) -> None:
        self.data.update({key: value})
        self._save_config()

    def get_entry(self, key: str) -> str:
        return self.data.get(key)

    # Remove an entry in program memory and config file
    def remove_entry(self, key: str) -> None:
        self.data.pop(key)
        self._save_config()


