import os
import json
from mcp.server.fastmcp import FastMCP
from mcp.server.session import ServerSession
from typing import Dict, Any, List, Optional

# Import your tools from tools.py here
from tools import (
    personalize_outline,
    generate_chapter,
    duplicate_template,
    inject_chapter,
    generate_book
)

# Create an MCP server
mcp = FastMCP("chapter-book-generator")

# Create a tool function for each tool you want to use
@mcp.tool()
def chapter_book_generator_personalize_outline(generic_outline: str, child_info: str, book_title: str, model: str = "claude-sonnet-4-20250514") -> str:
    """ Put in some text & a structured input & get a repsponse

    Args:
        input: The input text to process
        structured_input: A structured input to process

    Returns:
        A formatted string response.  
    """
    return(personalize_outline(generic_outline, child_info, book_title, model))

@mcp.tool()
def chapter_book_generator_duplicate_template(template_filename: str, book_title: str) -> str:
    """
    Creates a new book file from the template with the book title as the filename.
    
    Args:
        template_filename (str): Name of the template file (e.g., "Book Template.docx")
        book_title (str): The title of the book (used for filename)
    
    Returns:
        str: Path to the newly created book file
    """
    return(duplicate_template(template_filename, book_title))

@mcp.tool()
def chapter_book_generator_generate_chapter(outline: str, chapter_number: int, model: str = "claude-sonnet-4-20250514") -> str:
    """
    Generates a chapter of a children's chapter book using Claude.

    Args:
        outline: the tailored personal outline created with the personal outline tool
        chapter_number: the integer denoting which chapter should be generated from the outline
        model: the LLM to use for chapter generation

    Returns:
        A fully written chapter for the desired chapter number between 700-800 words long.
    """
    return(generate_chapter(outline, chapter_number, model))

@mcp.tool()
def chapter_book_generator_inject_chapter(book_file_name: str, chapter_content: str, chapter_number: int, chapter_title: str) -> str:
    """
    Injects a chapter into the book file created by the duplicate template tool.
    """
    return(inject_chapter(book_file_name, chapter_content, chapter_number, chapter_title))

@mcp.tool()
def generate_book(generic_outline: str, child_info: str, book_title: str, model: str = "claude-sonnet-4-20250514") -> str:
    """
    Generates a complete 10-chapter children's book using Claude.
    """
    return(generate_book(generic_outline, child_info, book_title, model))

# Run the server
if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run()