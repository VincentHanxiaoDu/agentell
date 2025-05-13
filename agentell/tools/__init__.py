from typing import Protocol, TypeVar, ParamSpec, Callable
import abc
import inspect
from fastmcp import FastMCP

P = ParamSpec("P")
R = TypeVar("R")


class BaseFunctionTool(Protocol[P, R]):
    """Base function tool class."""

    name: str
    description: str

    @classmethod
    def signature(cls) -> inspect.Signature:
        return inspect.signature(cls.__call__)

    @staticmethod
    @abc.abstractmethod
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...

    @classmethod
    def register_to_mcp(cls, mcp: FastMCP):
        mcp.add_tool(cls.__call__, name=cls.name, description=cls.description)
