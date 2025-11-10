"""
Ollama Client for C# Code Reviewer

This module provides a client for interacting with the Ollama LLM server.
It supports streaming responses, error handling, and retry logic.
"""

import ollama
import time
from typing import Generator, Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaClientError(Exception):
    """Base exception for Ollama client errors"""
    pass


class OllamaConnectionError(OllamaClientError):
    """Raised when connection to Ollama server fails"""
    pass


class ModelNotFoundError(OllamaClientError):
    """Raised when the requested model is not available"""
    pass


class PromptTooLongError(OllamaClientError):
    """Raised when prompt exceeds context window"""
    pass


class OllamaClient:
    """
    Client for interacting with Ollama LLM server.

    Attributes:
        model_name (str): Name of the LLM model to use
        host (str): Ollama server host URL
        timeout (int): Request timeout in seconds
        temperature (float): LLM temperature parameter
        top_p (float): LLM top_p parameter
    """

    def __init__(
        self,
        model_name: str = "phi3:mini",
        host: str = "http://localhost:11434",
        timeout: int = 30,
        temperature: float = 0.7,
        top_p: float = 0.9
    ):
        """
        Initialize Ollama client.

        Args:
            model_name: Name of the model to use (default: phi3:mini)
            host: Ollama server URL (default: http://localhost:11434)
            timeout: Request timeout in seconds (default: 30)
            temperature: LLM temperature (default: 0.7)
            top_p: LLM top_p parameter (default: 0.9)
        """
        self.model_name = model_name
        self.host = host
        self.timeout = timeout
        self.temperature = temperature
        self.top_p = top_p

        # Initialize Ollama client
        self.client = ollama.Client(host=host)

        logger.info(f"Initialized OllamaClient with model: {model_name}, host: {host}")

    def test_connection(self) -> bool:
        """
        Test connection to Ollama server.

        Returns:
            bool: True if connection successful, False otherwise

        Raises:
            OllamaConnectionError: If connection fails
        """
        try:
            # Try to list available models
            models_response = self.client.list()
            models = models_response.models if hasattr(models_response, 'models') else []
            logger.info(f"Connection successful. Available models: {len(models)}")

            # Check if our model is available
            model_names = [str(m.model) for m in models if m.model]
            if self.model_name not in model_names:
                logger.warning(f"Model {self.model_name} not found in available models: {model_names}")
                raise ModelNotFoundError(
                    f"Model '{self.model_name}' not found. "
                    f"Available models: {', '.join(model_names)}"
                )

            return True

        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            raise OllamaConnectionError(f"Failed to connect to Ollama server at {self.host}: {e}")

    def analyze_code(
        self,
        prompt: str,
        stream: bool = True,
        max_retries: int = 3
    ) -> Generator[str, None, None] | str:
        """
        Analyze code using LLM.

        Args:
            prompt: The prompt to send to LLM
            stream: Whether to stream the response (default: True)
            max_retries: Maximum number of retry attempts (default: 3)

        Returns:
            Generator yielding response tokens if stream=True, otherwise complete response string

        Raises:
            OllamaConnectionError: If connection fails after retries
            PromptTooLongError: If prompt exceeds context window
        """
        for attempt in range(max_retries):
            try:
                if stream:
                    return self._stream_response(prompt)
                else:
                    return self._get_response(prompt)

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")

                if attempt < max_retries - 1:
                    # Exponential backoff: 1s, 2s, 4s
                    wait_time = 2 ** attempt
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"All {max_retries} attempts failed")
                    raise OllamaConnectionError(f"Failed to get LLM response after {max_retries} attempts: {e}")

    def _stream_response(self, prompt: str) -> Generator[str, None, None]:
        """
        Stream response from LLM.

        Args:
            prompt: The prompt to send

        Yields:
            str: Response tokens
        """
        try:
            logger.info(f"Sending streaming request to {self.model_name}")
            start_time = time.time()

            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                stream=True,
                options={
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "num_predict": 4096  # Max tokens to generate (increased for full code rewrite)
                }
            )

            for chunk in response:
                token = chunk.get('response', '')
                if token:
                    yield token

            elapsed = time.time() - start_time
            logger.info(f"Streaming response completed in {elapsed:.2f} seconds")

        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            raise

    def _get_response(self, prompt: str) -> str:
        """
        Get complete response from LLM (non-streaming).

        Args:
            prompt: The prompt to send

        Returns:
            str: Complete response text
        """
        try:
            logger.info(f"Sending non-streaming request to {self.model_name}")
            start_time = time.time()

            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                stream=False,
                options={
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "num_predict": 4096  # Max tokens to generate (increased for full code rewrite)
                }
            )

            elapsed = time.time() - start_time
            response_text = response.get('response', '')
            logger.info(f"Response received in {elapsed:.2f} seconds ({len(response_text)} chars)")

            return response_text

        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the currently loaded model.

        Returns:
            Dict containing model information
        """
        try:
            models_response = self.client.list()
            models = models_response.models if hasattr(models_response, 'models') else []

            for model in models:
                if model.model == self.model_name:
                    return {
                        'name': model.model,
                        'size': model.size,
                        'modified_at': str(model.modified_at),
                        'digest': model.digest,
                        'details': {
                            'parameter_size': model.details.parameter_size if model.details else 'N/A',
                            'quantization_level': model.details.quantization_level if model.details else 'N/A',
                            'format': model.details.format if model.details else 'N/A',
                            'family': model.details.family if model.details else 'N/A'
                        }
                    }

            raise ModelNotFoundError(f"Model {self.model_name} not found")

        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            raise


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = OllamaClient(model_name="phi3:mini")

    # Test connection
    try:
        client.test_connection()
        print("✓ Connection test passed!")
    except OllamaClientError as e:
        print(f"✗ Connection test failed: {e}")
        exit(1)

    # Test simple code review
    test_prompt = """
    당신은 C# 코드 리뷰 전문가입니다. 다음 코드를 분석하고 문제점을 찾아주세요.

    코드:
    ```csharp
    public class Example
    {
        public void ProcessData(string data)
        {
            var result = data.ToUpper();
            Console.WriteLine(result);
        }
    }
    ```

    문제점을 간단히 설명해주세요.
    """

    print("\n" + "="*50)
    print("Testing LLM Response (Streaming)...")
    print("="*50 + "\n")

    try:
        for token in client.analyze_code(test_prompt, stream=True):
            print(token, end='', flush=True)
        print("\n")
    except OllamaClientError as e:
        print(f"Error: {e}")

    # Get model info
    print("\n" + "="*50)
    print("Model Information:")
    print("="*50)
    try:
        model_info = client.get_model_info()
        print(f"Name: {model_info['name']}")
        print(f"Size: {model_info['size'] / 1e9:.2f} GB")
        print(f"Modified: {model_info['modified_at']}")
        if 'details' in model_info:
            details = model_info['details']
            print(f"Parameters: {details.get('parameter_size', 'N/A')}")
            print(f"Quantization: {details.get('quantization_level', 'N/A')}")
    except OllamaClientError as e:
        print(f"Error: {e}")
