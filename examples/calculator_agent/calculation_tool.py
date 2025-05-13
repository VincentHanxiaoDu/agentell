from typing import Annotated, Optional

from pydantic import Field
from agentell.tools import BaseFunctionTool
from fastmcp import FastMCP


class CalculationTool(BaseFunctionTool[str, float]):

    name = "calculation"

    description = "A tool for calculating the result of a calculation"

    @staticmethod
    def __call__(expression: Annotated[str, Field(description="The expression to calculate in python")]) -> float:
        return eval(expression)

if __name__ == "__main__":
    mcp = FastMCP("Test MCP APP")
    CalculationTool.register_to_mcp(mcp)
    mcp.run(
        transport="sse",
        host="127.0.0.1",
        port=4200,
        log_level="debug",
        path="/sse",
    )
