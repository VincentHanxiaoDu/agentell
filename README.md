# Agentell

Agentell is a framework for building intelligent agent-based systems using large language models (LLMs).

## Features

- Agent abstractions for both synchronous and asynchronous workflows
- Memory management for agent interactions
- Tool integration system with type-safe interfaces
- LLM provider compatibility layer
- Calculator utilities for working with mathematical operations

## Installation

```bash
pip install agentell
```

## Examples

Check out our examples to see AgentEll in action:

### Calculator Agent

Located in `examples/calculator_agent/`, this example demonstrates:

E.g., to run the calculator agent:

1. Run the MCP server first

    ```bash
    python -m examples.calculator_agent.calculation_tool
    ```

2. Run the calculator agent in REPL

    ```bash
    export OPENROUTER_API_KEY=<your-openrouter-api-key>
    python -m examples.calculator_agent.calculator_agent
    ```
