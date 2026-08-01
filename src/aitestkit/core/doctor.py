import importlib.util
import platform
import sys
import psutil

class HealthDoctor:
    """System health check and diagnostic tool."""

    @staticmethod
    def run_diagnostics() -> dict:
        results = {}
        
        # 1. Environment Info
        results["python_version"] = sys.version.split()[0]
        results["os"] = platform.system()
        results["ram_gb"] = round(psutil.virtual_memory().total / (1024**3), 2)

        # 2. Framework Detections
        deps = ["torch", "openai", "langchain", "llama_index", "chromadb", "faiss", "psutil", "streamlit"]
        installed_deps = {}
        for dep in deps:
            installed_deps[dep] = importlib.util.find_spec(dep) is not None
        results["dependencies"] = installed_deps

        # 3. GPU Diagnostic
        try:
            import torch
            results["gpu_available"] = torch.cuda.is_available()
            results["gpu_name"] = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None"
        except ImportError:
            results["gpu_available"] = False
            results["gpu_name"] = "N/A (PyTorch not installed)"

        return results