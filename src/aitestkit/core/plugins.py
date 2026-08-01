import importlib.util

class PluginManager:
    """Dynamically detects and registers installed external AI evaluation plugins."""

    PLUGINS = ["ragas", "deepeval", "langsmith", "promptfoo", "trulens", "phoenix"]

    @classmethod
    def detect_installed_plugins(cls) -> list[str]:
        installed = []
        for plugin in cls.PLUGINS:
            spec = importlib.util.find_spec(plugin)
            if spec is not None:
                installed.append(plugin)
        return installed