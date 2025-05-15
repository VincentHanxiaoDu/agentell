import json
import requests
import logging
from agentell.extern.api.openai.compat import OpenAICompatAPI

logger = logging.getLogger(__name__)


class OpenRouterChatLLM(OpenAICompatAPI):
    """OpenRouter Chat API."""

    def __init__(self, model: str, api_key: str):
        super().__init__(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        self._model = model
        self._headers = self._auth_header

    @staticmethod
    def parse_http_stream(response: requests.Response, chunk_size=1024):
        """Parse the HTTP stream response from OpenRouter.

        Args:
            response: The SSE response from OpenRouter.
            chunk_size: The chunk size to use for the response.

        Returns:
            A generator of data objects.
        """
        response.encoding = "utf-8"
        buffer = ""
        for chunk in response.iter_content(chunk_size=chunk_size):
            buffer += chunk.decode("utf-8")
            while True:
                try:
                    line_end = buffer.find("\n")
                    if line_end == -1:
                        break
                    line = buffer[:line_end].strip()
                    buffer = buffer[line_end + 1 :]
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            data_obj = json.loads(data)
                            yield data_obj
                        except json.JSONDecodeError:
                            pass
                except Exception:
                    break

    @staticmethod
    def get_formatted_http_stream(parsed_http_stream):
        """Format the HTTP stream response from OpenRouter to be used by the agent.

        Args:
            response: The SSE response from OpenRouter.
            chunk_size: The chunk size to use for the response.

        Returns:
            A generator of formatted chunks, a dict with the type of the chunk and the data.
            The type can be:
                - "chat.completion.chunk": A chunk of the chat completion.
                - "tool_calls": A list of tool calls.
        """
        all_tool_calls = {}
        for chunk in parsed_http_stream:
            if "error" in chunk:
                raise RuntimeError(chunk)
            msg_id = chunk["id"]
            first_choice = next(filter(lambda x: x["index"] == 0, chunk["choices"]))
            for tool_call in first_choice["delta"].get("tool_calls", []):
                tool_call_id = (msg_id, tool_call["index"])
                if tool_call_id not in all_tool_calls:
                    all_tool_calls[tool_call_id] = tool_call
                    if (
                        all_tool_calls[tool_call_id]["function"].get("arguments")
                        is None
                    ):
                        all_tool_calls[tool_call_id]["function"]["arguments"] = ""
                else:
                    all_tool_calls[tool_call_id]["function"]["arguments"] += tool_call[
                        "function"
                    ]["arguments"]
            if first_choice["delta"].get("content"):
                yield {
                    "type": "chat.completion.chunk",
                    "data": first_choice["delta"]["content"],
                }
        yield {"type": "tool_calls", "data": list(all_tool_calls.values())}

    def completions(self, prompt, stream=False, retry: int = 3, **kwargs):
        total_retry = retry
        exception = None
        while retry > 0:
            try:
                response = requests.post(
                    url=self._completions_url,
                    headers=self._headers,
                    data=json.dumps(
                        {
                            "model": self._model,
                            "messages": prompt,
                            "stream": stream,
                            **kwargs,
                        }
                    ),
                    stream=stream,
                )
                response.raise_for_status()
                return response
            except Exception as e:
                retry -= 1
                exception = e
                logger.error(
                    f"OpenRouter API Error: {e}, retry: {total_retry - retry} / {total_retry}"
                )
        raise exception
