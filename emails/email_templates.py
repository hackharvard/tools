from abc import ABC, abstractmethod
from pathlib import Path
import json
import html
import re
from datetime import date
from functools import partial

def get_template(name: str) -> "EmailTemplate":
    templates = {
        "general": GeneralEmailTemplate,
        "action": ActionEmailTemplate,
    }
    if name not in templates:
        raise ValueError(f"Unknown template: {name}")
    return templates[name]()

class EmailTemplate(ABC):
    def __init__(self, config_path: str | Path = "base.json") -> None:
        self.logo_url = "https://raw.githubusercontent.com/hackharvard/branding/refs/heads/main/static/logoForEmailNoBg.png"
        self.theme_color = "#e20029"
        self.background_color = "#f8f8f8"
        self.footer_year = date.today().year

        p = Path(config_path)
        if p.is_file():
            with p.open("r", encoding="utf-8") as f:
                cfg = json.load(f)
            self.logo_url = cfg.get("logo_url", self.logo_url)
            self.theme_color = cfg.get("theme_color", self.theme_color)
            self.background_color = cfg.get("background_color", self.background_color)
            self.footer_year = cfg.get("footer_year", self.footer_year)

    def paragraphize(self, text: str) -> str:
        safe = html.escape(text.strip(), quote=True)
        parts = re.split(r"\r?\n\s*\r?\n", safe)  # handles \n or \r\n and extra whitespace
        parts = [p.replace("\r\n", "\n").replace("\n", "<br>") for p in parts]
        return "".join(f"<p>{p}</p>" for p in parts if p)
    
    @staticmethod
    def compile_template(template: str, mapping: dict[str, str]) -> str:
        """Replaces all keys in `mapping` with their corresponding values in the `template` string."""
        if not mapping:
            return template
        keys = sorted(mapping.keys(), key=len, reverse=True)
        pattern = re.compile("|".join(re.escape(k) for k in keys))
        return pattern.sub(lambda m: mapping[m.group(0)], template)

    @abstractmethod
    def build(self, *args, **kwargs) -> str:
        """Returns an HTML string that is constructed from the given parameters."""
        raise NotImplementedError

class GeneralEmailTemplate(EmailTemplate):
    path = Path("emails/html/general.html")

    def build(
        self,
        *,
        title: str,
        description: str,
        app_name: str,
        app_link: str,
        extra_html: str = ""
    ) -> str:
        esc = partial(html.escape, quote=True)
        tpl = self.path.read_text(encoding="utf-8")

        mapping = {
            "{{title}}": esc(title),
            "{{description}}": self.paragraphize(description),
            "{{app.name}}": esc(app_name),
            "{{app.link}}": esc(app_link),
            "{{extra.html}}": extra_html or "",
            "{{cfg.logo_url}}": esc(self.logo_url),
            "{{cfg.theme_color}}": esc(self.theme_color),
            "{{cfg.background_color}}": esc(self.background_color),
            "{{cfg.footer_year}}": str(self.footer_year),
        }
        return self.compile_template(tpl, mapping)

class ActionEmailTemplate(EmailTemplate):
    path = Path("emails/html/action.html")

    def build(
        self,
        *,
        title: str,
        description: str,
        action_link: str,
        action_buttonname: str,
        app_name: str,
        app_link: str,
        extra_html: str = ""
    ) -> str:
        esc = partial(html.escape, quote=True)
        tpl = self.path.read_text(encoding="utf-8")

        mapping = {
            "{{title}}": esc(title),
            "{{description}}": self.paragraphize(description),
            "{{action.link}}": esc(action_link),
            "{{action.buttonname}}": esc(action_buttonname),
            "{{app.name}}": esc(app_name),
            "{{app.link}}": esc(app_link),
            "{{extra.html}}": extra_html or "",
            "{{cfg.logo_url}}": esc(self.logo_url),
            "{{cfg.theme_color}}": esc(self.theme_color),
            "{{cfg.background_color}}": esc(self.background_color),
            "{{cfg.footer_year}}": str(self.footer_year),
        }
        
        return self.compile_template(tpl, mapping)
    