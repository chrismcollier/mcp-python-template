import os
import json
from mcp.server.fastmcp import FastMCP
from mcp.server.session import ServerSession
from typing import Dict, Any, List, Optional

# Import your tools from tools.py here
from tools import (
    tool_name
)

# Create an MCP server
mcp = FastMCP("Example Agent")

# Create a tool function for each tool you want to use
@mcp.tool()
def tool_name(input: str, structured_input: Optional[Dict[str, Any]] = None) -> str:
    """ Put in some text & a structured input & get a repsponse

    Args:
        input: The input text to process
        structured_input: A structured input to process

    Returns:
        A formatted string response.  
    """
    return(tool_name(input, structured_input))


# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")