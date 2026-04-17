import qdarktheme

from theme.adwaita_stylesheet import adwaita_dark, adwaita_light

class Theme():
    def __init__(self):
        # Style lists for themes
        self.dark_theme_map = { 
            "fusion": qdarktheme.load_stylesheet("dark"),
            "adwaita": adwaita_dark
        }
        self.light_theme_map = {
            "fusion": qdarktheme.load_stylesheet("light"),
            "adwaita": adwaita_light  
        }
        self.themes = [
            "fusion",
            "adwaita",
        ]

    def get_theme_list(self):
        return self.themes

    def get_stylesheet(self, theme: str, mode: str):
        if mode == "light":
            return self.light_theme_map.get(theme)
        elif mode == "dark":
            return self.dark_theme_map.get(theme)
        else:
            raise Exception(f"[ERROR] Invalid theme parameter given to get_stylesheet of {theme}")



