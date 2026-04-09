import shutil
import os
from platformdirs import user_config_dir

class HandleConfig():
    def _initialize():
        app_name = "SuperDuperSecret"
        app_author = "SuperDuperSecret"

        config_dir = user_config_dir(app_name, app_author)

        # Ensure config directories exist
        os.makedires(config_dir, exist_ok=True)

        config_path = os.path.join(config_dir, "settings.json")

        return {"config_dir": config_dir, "config_path": config_path}

    @staticmethod
    def save(data: dict) -> None:
        config_path = _initialize()["config_path"]

        try:
            with open(config_path, "w") as f:
                json.dump(data, f)
            print(f"[INFO] Config saved to: {config_path}")
        except Exception as e:
            print(f"[ERROR] Could not load config from: {config_path}")

    # Returns an empty dictionary if config file does not exist
    # Returns the config as a dictionary if the config file exists
    @staticmethod
    def load() -> dict:
        config_path = _initialize()["config_path"]
        
        if not os.path.exists(config_path):
            return {}

        with open(config_path, "r") as f:
            data = json.load(f)
            return data

    @staticmethod
    def delete_config():
        config_dir = _initialize()["config_dir"]

        print(f"[WARNING] This will delete everything within {config_dir}")
        authorize = input("Proceed? (y/N) > ")

        if authorize.lower() == "y":
            try:
                if os.path.exists(config_dir):
                    shutil.rmtree(config_dir)
                    print(f"[INFO] Deleted: {config_dir}")
                else:
                    print("[INFO] Did not delete config as it does not exist.")
            except Exception as e:
                print(f"[ERROR] Could not delete: {config_dir}")
        else:
            print("operation canceled")