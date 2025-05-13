from agentell.extern.api.openai.compat import OpenAICompatAPI


class OpenAICompatChatAPI(OpenAICompatAPI):
    """OpenAI compat chat API."""

    def __init__(self, api_key: str, base_url: str):
        super().__init__(api_key=api_key, base_url=base_url)
        self._completions_url = f"{self._base_url}/chat/completions"
