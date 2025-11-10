"""
Ollama Process Manager

Manages Ollama server lifecycle for portable deployments.
Automatically starts Ollama when the application launches and stops it on exit.
"""

import os
import sys
import time
import subprocess
import signal
import logging
from pathlib import Path
from typing import Optional
import requests


logger = logging.getLogger(__name__)


class OllamaManager:
    """
    Manages Ollama server process lifecycle

    Features:
    - Auto-start Ollama on application launch
    - Auto-stop on application exit
    - Health check and retry logic
    - Support for both system Ollama and portable version
    """

    def __init__(
        self,
        ollama_host: str = "http://localhost:11434",
        portable_path: Optional[Path] = None,
        startup_timeout: int = 30,
        model_name: str = "phi3:mini"
    ):
        """
        Initialize Ollama manager

        Args:
            ollama_host: Ollama server URL
            portable_path: Path to portable Ollama (e.g., ./ollama_portable/ollama.exe)
            startup_timeout: Max seconds to wait for Ollama to start
            model_name: Model to verify is available
        """
        self.ollama_host = ollama_host
        self.portable_path = portable_path
        self.startup_timeout = startup_timeout
        self.model_name = model_name
        self.process: Optional[subprocess.Popen] = None
        self._is_managed = False  # Whether we started Ollama ourselves

    def is_running(self) -> bool:
        """Check if Ollama server is accessible"""
        try:
            response = requests.get(
                f"{self.ollama_host}/api/tags",
                timeout=2
            )
            return response.status_code == 200
        except Exception:
            return False

    def has_model(self) -> bool:
        """Check if required model is available"""
        try:
            response = requests.get(
                f"{self.ollama_host}/api/tags",
                timeout=2
            )
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                return any(
                    model.get("name", "").startswith(self.model_name)
                    for model in models
                )
            return False
        except Exception:
            return False

    def start(self) -> bool:
        """
        Start Ollama server if not already running

        Returns:
            True if Ollama is running (either already running or successfully started)
        """
        # Check if already running
        if self.is_running():
            logger.info("Ollama is already running")
            return True

        # Try to start portable Ollama if path provided
        if self.portable_path and self.portable_path.exists():
            logger.info(f"Starting portable Ollama from: {self.portable_path}")
            return self._start_portable()

        # Try to start system Ollama
        logger.info("Starting system Ollama...")
        return self._start_system()

    def _start_portable(self) -> bool:
        """Start portable Ollama executable"""
        try:
            # Set environment variables for portable mode
            env = os.environ.copy()

            # Set OLLAMA_MODELS to portable models directory
            models_dir = self.portable_path.parent / "models"
            if models_dir.exists():
                env["OLLAMA_MODELS"] = str(models_dir)
                logger.info(f"OLLAMA_MODELS set to: {models_dir}")

            # Start Ollama process
            if sys.platform == "win32":
                # Windows: Hide console window
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

                self.process = subprocess.Popen(
                    [str(self.portable_path), "serve"],
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                # macOS/Linux
                self.process = subprocess.Popen(
                    [str(self.portable_path), "serve"],
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

            self._is_managed = True
            logger.info(f"Ollama process started (PID: {self.process.pid})")

            # Wait for Ollama to be ready
            return self._wait_for_ready()

        except Exception as e:
            logger.error(f"Failed to start portable Ollama: {e}")
            return False

    def _start_system(self) -> bool:
        """Start system Ollama (ollama serve)"""
        try:
            # Try to find ollama in PATH
            if sys.platform == "win32":
                ollama_cmd = "ollama.exe"
            else:
                ollama_cmd = "ollama"

            # Start Ollama process
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

                self.process = subprocess.Popen(
                    [ollama_cmd, "serve"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.process = subprocess.Popen(
                    [ollama_cmd, "serve"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

            self._is_managed = True
            logger.info(f"System Ollama started (PID: {self.process.pid})")

            # Wait for Ollama to be ready
            return self._wait_for_ready()

        except FileNotFoundError:
            logger.error("Ollama executable not found in PATH")
            return False
        except Exception as e:
            logger.error(f"Failed to start system Ollama: {e}")
            return False

    def _wait_for_ready(self) -> bool:
        """Wait for Ollama server to be ready"""
        logger.info(f"Waiting for Ollama to be ready (timeout: {self.startup_timeout}s)...")

        start_time = time.time()
        while time.time() - start_time < self.startup_timeout:
            if self.is_running():
                logger.info("Ollama is ready!")

                # Check if model is available
                if self.has_model():
                    logger.info(f"Model '{self.model_name}' is available")
                    return True
                else:
                    logger.warning(f"Model '{self.model_name}' not found")
                    logger.warning("You may need to pull the model manually:")
                    logger.warning(f"  ollama pull {self.model_name}")
                    return True  # Still return True since server is running

            time.sleep(0.5)

        logger.error(f"Ollama failed to start within {self.startup_timeout}s")
        return False

    def stop(self):
        """Stop Ollama server if we started it"""
        if not self._is_managed or not self.process:
            logger.info("Ollama was not started by manager, skipping stop")
            return

        logger.info(f"Stopping Ollama process (PID: {self.process.pid})...")

        try:
            # Try graceful termination first
            if sys.platform == "win32":
                self.process.terminate()
            else:
                self.process.send_signal(signal.SIGTERM)

            # Wait up to 5 seconds for graceful shutdown
            try:
                self.process.wait(timeout=5)
                logger.info("Ollama stopped gracefully")
            except subprocess.TimeoutExpired:
                # Force kill if still running
                logger.warning("Ollama did not stop gracefully, force killing...")
                self.process.kill()
                self.process.wait()
                logger.info("Ollama force killed")

        except Exception as e:
            logger.error(f"Error stopping Ollama: {e}")

        finally:
            self.process = None
            self._is_managed = False

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
