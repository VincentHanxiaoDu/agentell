from agentell.agent import SyncAgent
from agentell.agent.agent_task import AgentTask
from agentell.utils.repl import REPLHandler
from agentell.extern.api.openai.compat.chat.openrouter import OpenRouterChatLLM
import asyncio
from fastmcp import Client
from fastmcp.client import SSETransport
import json
import mcp
import os


class CalculatorAgent(SyncAgent):
    def __init__(self, llm: OpenRouterChatLLM):
        super().__init__()
        self._llm = llm
        self.io_handler = REPLHandler()
        self.mcp_sse_url = "http://127.0.0.1:4200/sse"
        self.client_sse = None

    def start(self):
        self.client_sse = Client(SSETransport(self.mcp_sse_url))

    def _process(self, task: AgentTask):
        return asyncio.run(self._async_process(task))

    async def _async_process(self, task: AgentTask):
        prompt = [
            {
                "role": "system",
                "content": f"You are an agent that can answer the questions from the user in natural language, you can use the tools from the MCP server to get the information you need.",
            }
        ]
        async with self.client_sse:
            all_tools = await self.client_sse.list_tools()
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                        "strict": True,
                    },
                }
                for tool in all_tools
            ]
            while True:
                self.io_handler.push(">>> ", end="")
                user_input = self.io_handler.get_input()
                prompt.append({"role": "user", "content": user_input})
                while True:
                    llm_response = self._llm.completions(
                        prompt=prompt, stream=True, tools=tools, function_call="auto"
                    )
                    parsed_sse = OpenRouterChatLLM.parse_sse(llm_response)
                    is_responding = False
                    all_tool_calls = []
                    for chunk in OpenRouterChatLLM.get_formatted_sse(parsed_sse):
                        if chunk["type"] == "chat.completion.chunk":
                            self.io_handler.push(chunk["data"])
                            is_responding = True
                        elif chunk["type"] == "tool_calls":
                            all_tool_calls.extend(chunk["data"])
                    if all_tool_calls:
                        prompt.append(
                            {"role": "assistant", "tool_calls": all_tool_calls}
                        )
                    for tool_call in all_tool_calls:
                        self.io_handler.push(
                            f"Calling tool: {tool_call['function']['name']} with arguments: {tool_call['function']['arguments']}\n"
                        )
                        results = await self.client_sse.call_tool(
                            tool_call["function"]["name"],
                            json.loads(tool_call["function"]["arguments"]),
                        )
                        self.io_handler.push(
                            f"Tool {tool_call['function']['name']} returned: {results}\n"
                        )
                        for result in results:
                            if isinstance(result, mcp.types.TextContent):
                                prompt.append(
                                    {
                                        "role": "tool",
                                        "tool_call_id": tool_call["id"],
                                        "content": result.text,
                                    }
                                )
                            else:
                                raise RuntimeError(
                                    f"Unsupported content type: {type(result)}"
                                )
                    if is_responding:
                        self.io_handler.push("\n")
                        break

    def shutdown(self, timeout: float = 10):
        return super().shutdown(timeout)


if __name__ == "__main__":
    model = "openai/gpt-4.1"
    api_key = os.getenv("OPENROUTER_API_KEY")
    llm = OpenRouterChatLLM(model=model, api_key=api_key)
    with CalculatorAgent(llm=llm) as agent:
        task = AgentTask(name="calc", description="run math solver repl")
        agent.submit(task)
