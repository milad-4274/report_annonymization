import json
import logging
from typing import Any, Dict, Optional, Union
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMCaller:
    """A general client wrapper for local or remote OpenAI-compatible LLM endpoints.

    Compatible with: vLLM, Ollama, Triton, HuggingFace TGI, OpenAI, etc.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434/v1",  # Default: Ollama local endpoint
        api_key: str = "ollama",                       # Any string works for local endpoints
        model_name: str = "qwen2.5:7b",
        temperature: float = 0.0,                      # Low temp for deterministic/extraction tasks
        max_tokens: int = 2048,
    ):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        json_mode: bool = False,
        **kwargs,
    ) -> str:
        """Sends a text generation request to the LLM backend with auto-retry logic.

        Args:
            prompt: User prompt/input text.
            system_prompt: System role instructions.
            json_mode: Forces JSON schema output if supported by the provider.
            **kwargs: Overrides default generation parameters (temperature, top_p, etc.)

        Returns:
            String response from the LLM.
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response_format = {"type": "json_object"} if json_mode else None

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=kwargs.get("temperature", self.temperature),
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                response_format=response_format,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error calling LLM endpoint ({self.model_name}): {e}")
            raise e

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Utility method to get and safely parse a JSON response from the LLM."""
        raw_output = self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            json_mode=True,
        )
        try:
            return json.loads(raw_output)
        except json.JSONDecodeError:
            # Fallback cleanup for models that wrap JSON in markdown code blocks
            clean_output = raw_output.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_output)

