# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""analyze-paper-agent - An Bindu Agent."""

import argparse
import asyncio
import json
import os
from pathlib import Path
from textwrap import dedent
from typing import Any

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.arxiv import ArxivTools
from agno.tools.mcp import MultiMCPTools
from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global MCP tools instances
mcp_tools: MultiMCPTools | None = None
agent: Agent | None = None
model_name: str | None = None
api_key: str | None = None
mem0_api_key: str | None = None
_initialized = False
_init_lock = asyncio.Lock()


async def initialize_mcp_tools(env: dict[str, str] | None = None) -> None:
    """Initialize and connect to MCP servers.

    Args:
        env: Environment variables dict for MCP servers (e.g., API keys)
    """
    global mcp_tools

    # Initialize MultiMCPTools with all MCP server commands
    # TODO: Add your MCP server commands here
    mcp_tools = MultiMCPTools(
        commands=[
            "npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt",
            "npx -y @modelcontextprotocol/server-google-maps",
        ],
        env=env or dict(os.environ),  # Use provided env or fall back to os.environ
        allow_partial_failure=True,  # Don't fail if one server is unavailable
        timeout_seconds=30,
    )

    # Connect to all MCP servers
    await mcp_tools.connect()
    print("✅ Connected to MCP servers")


def load_config() -> dict:
    """Load agent configuration from project root."""
    # Get path to agent_config.json in project root
    config_path = Path(__file__).parent / "agent_config.json"

    with open(config_path) as f:
        return json.load(f)


# Create the agent instance
async def initialize_agent() -> None:
    """Initialize the agent once."""
    global agent, model_name, mcp_tools

    if not model_name:
        msg = "model_name must be set before initializing agent"
        raise ValueError(msg)

    agent = Agent(
        name="analyze-paper-agent Bindu Agent",
        model=OpenRouter(
            id=model_name,
            api_key=api_key,
            cache_response=True,
            supports_native_structured_outputs=True,
        ),
        tools=[tool for tool in [mcp_tools, ArxivTools(all=True)] if tool is not None],  # MultiMCPTools instance
        instructions=[
            dedent("""\
            # IDENTITY and PURPOSE
You are an objectively minded and centrist-oriented analyzer of truth claims and arguments.

You specialize in analyzing and rating the truth claims made in the input provided and providing both evidence in support of those claims, as well as counter-arguments and counter-evidence that are relevant to those claims.

You also provide a rating for each truth claim made.

The purpose is to provide a concise and balanced view of the claims made in a given piece of input so that one can see the whole picture.

Take a step back and think step by step about how to achieve the best possible output given the goals above.

# Steps

- Deeply analyze the truth claims and arguments being made in the input.
- Separate the truth claims from the arguments in your mind.

# OUTPUT INSTRUCTIONS

- Provide a summary of the argument being made in less than 30 words in a section called ARGUMENT SUMMARY:.

- In a section called TRUTH CLAIMS:, perform the following steps for each:

1. List the claim being made in less than 16 words in a subsection called CLAIM:.
2. Provide solid, verifiable evidence that this claim is true using valid, verified, and easily corroborated facts, data, and/or statistics. Provide references for each, and DO NOT make any of those up. They must be 100% real and externally verifiable. Put each of these in a subsection called CLAIM SUPPORT EVIDENCE:.

3. Provide solid, verifiable evidence that this claim is false using valid, verified, and easily corroborated facts, data, and/or statistics. Provide references for each, and DO NOT make any of those up. They must be 100% real and externally verifiable. Put each of these in a subsection called CLAIM REFUTATION EVIDENCE:.

4. Provide a list of logical fallacies this argument is committing, and give short quoted snippets as examples, in a section called LOGICAL FALLACIES:.

5. Provide a CLAIM QUALITY score in a section called CLAIM RATING:, that has the following tiers:
   A (Definitely True)
   B (High)
   C (Medium)
   D (Low)
   F (Definitely False)

6. Provide a list of characterization labels for the claim, e.g., specious, extreme-right, weak, baseless, personal attack, emotional, defensive, progressive, woke, conservative, pandering, fallacious, etc., in a section called LABELS:.

- In a section called OVERALL SCORE:, give a final grade for the input using the same scale as above. Provide three scores:

LOWEST CLAIM SCORE:
HIGHEST CLAIM SCORE:
AVERAGE CLAIM SCORE:

- In a section called OVERALL ANALYSIS:, give a 30-word summary of the quality of the argument(s) made in the input, its weaknesses, its strengths, and a recommendation for how to possibly update one's understanding of the world based on the arguments provided.
        """)
        ],
        add_datetime_to_context=True,
        markdown=True,
    )
    print("✅ Agent initialized")


async def cleanup_mcp_tools() -> None:
    """Close all MCP server connections."""
    global mcp_tools

    if mcp_tools:
        try:
            await mcp_tools.close()
            print("🔌 Disconnected from MCP servers")
        except Exception as e:
            print(f"⚠️  Error closing MCP tools: {e}")


async def run_agent(messages: list[dict[str, str]]) -> Any:
    """Run the agent with the given messages.

    Args:
        messages: List of message dicts with 'role' and 'content' keys

    Returns:
        Agent response
    """
    global agent

    # Run the agent and get response
    response = await agent.arun(messages)
    return response


async def handler(messages: list[dict[str, str]]) -> Any:
    """Handle incoming agent messages.

    Args:
        messages: List of message dicts with 'role' and 'content' keys
                  e.g., [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]

    Returns:
        Agent response (ManifestWorker will handle extraction)
    """
    # Run agent with messages
    global _initialized

    # Lazy initialization on first call (in bindufy's event loop)
    async with _init_lock:
        if not _initialized:
            print("🔧 Initializing MCP tools and agent...")
            # Build environment with API keys
            env = {
                **os.environ,
                # "GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY", ""),
            }
            await initialize_all(env)
            _initialized = True

    # Run the async agent
    result = await run_agent(messages)
    return result


async def initialize_all(env: dict[str, str] | None = None):
    """Initialize MCP tools and agent.

    Args:
        env: Environment variables dict for MCP servers
    """
    # await initialize_mcp_tools(env)
    await initialize_agent()


def main():
    """Run the Agent."""
    global model_name, api_key, mem0_api_key

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Bindu Agent with MCP Tools")
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_NAME", "openai/gpt-5.2-chat"),
        help="Model ID to use (default: openai/gpt-5.2-chat, env: MODEL_NAME), if you want you can use any free model: https://openrouter.ai/models?q=free",
    )

    parser.add_argument(
        "--api-key",
        type=str,
        default=os.getenv("OPENROUTER_API_KEY"),
        help="OpenRouter API key (env: OPENROUTER_API_KEY)",
    )
    parser.add_argument(
        "--mem0-api-key",
        type=str,
        default=os.getenv("MEM0_API_KEY"),
        help="Mem0 API key (env: MEM0_API_KEY)",
    )
    args = parser.parse_args()

    # Set global model name and API keys
    model_name = args.model
    api_key = args.api_key
    mem0_api_key = args.mem0_api_key

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY required")  # noqa: TRY003
    if not mem0_api_key:
        raise ValueError("MEM0_API_KEY required. Get your API key from: https://app.mem0.ai/dashboard/api-keys")  # noqa: TRY003

    print(f"🤖 Using model: {model_name}")
    print("🧠 Mem0 memory enabled")

    # Load configuration
    config = load_config()

    try:
        # Bindufy and start the agent server
        # Note: MCP tools and agent will be initialized lazily on first request
        print("🚀 Starting Bindu agent server...")
        bindufy(config, handler)
    finally:
        # Cleanup on exit
        print("\n🧹 Cleaning up...")
        asyncio.run(cleanup_mcp_tools())


# Bindufy and start the agent server
if __name__ == "__main__":
    main()
