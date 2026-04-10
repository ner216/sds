import shutil
import os
from platformdirs import user_config_dir

class Config():
    def __init__(self):
        self.data = {}

        app_name = "SuperDuperSecret"
        app_author = "SuperDuperSecret"

        self.config_dir = user_config_dir(app_name, app_author)

        # Ensure config directories exist
        os.makedirs(self.config_dir, exist_ok=True)

        self.config_path = os.path.join(self.config_dir, "settings.json")
        self.default_safe_path = os.path.join(self.config_dir, "default-safe.json")

    def save(self) -> None:
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.data, f)
            print(f"[INFO] Config saved to: {self.config_path}")
        except Exception as e:
            print(f"[ERROR] Could not load config from: {self.config_path}")

    # Returns an empty dictionary if config file does not exist
    # Returns the config as a dictionary if the config file exists
    def load(self):
        if not os.path.exists(self.config_path):
            self.data = {}

        with open(self.config_path, "r") as f:
            self.data = json.load(f)

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

    def get_default_safe_path(self):
        return self.default_safe_path