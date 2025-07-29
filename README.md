# **MCP Python Server Template**
A production-ready template for building Model Context Protocol (MCP) servers in Python.
This template provides a starting place to clone & setup your own MCP servers with tools.

## **Prerequisites:**
- Python 3.8 or higher
- pip or poetry for package management
- Git for version control

# **Quick Start:**

## **Clone and Setup**
1. bash# Clone the template
2. git clone https://github.com/yourusername/mcp-python-template.git my-mcp-server
3. cd my-mcp-server

## **Remove the template's git history and initialize your own**
- rm -rf .git
- git init
- git add .
- git commit -m "Initial commit from MCP template"

## Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## Install dependencies
pip install -r requirements.txt

## **Customize to your use case:**
1. Edit your Claude config.json file to support the connections you need:

   
        {
            "mcpServers": {
                "mcpName": {
                    "command": "src/venv/bin/python3"
                    "args": ["src/server.py"]
                    "env": {
                        api keys & secrets
                    }
                }
            }
        }
3. Add your tools in src/tools.py
    Replace the example tools with your own
    Update the tool schemas and descriptions
4. Modify the server.py file with your tools
    Import your new tools in the example list in the server.py file
    Create a function call with descriptions for each new tool you add
