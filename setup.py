from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip()]

setup(
    name="agentell",
    version="0.1.0",
    author="AgentEll Team",
    author_email="info@agentell.com",
    description="An agent-based intelligent system framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["agentell", "agentell.*"]),
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="ai, agent, llm, tools, automation",
)
