# Children's Chapter Book Generator - Setup Guide

## Overview
This application generates personalized children's chapter books using AI. It includes:
- Web interface for input collection
- Genre and plot selection (Sci-fi, Fantasy, Mystery, Adventure)
- Child information personalization
- Document upload for training AI with your writing style
- Template-based book generation using Word documents

## Prerequisites
- Python 3.8 or higher
- pip package manager
- Anthropic API key (for Claude AI)

## Installation Steps

### 1. Clone/Navigate to Project Directory
```bash
cd chapter-book-generator
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Environment Variables
Create a `.env` file or set environment variable:
```bash
# Option 1: Create .env file
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env

# Option 2: Set environment variable (Windows)
set ANTHROPIC_API_KEY=your-api-key-here

# Option 2: Set environment variable (macOS/Linux)
export ANTHROPIC_API_KEY=your-api-key-here
```

### 6. Prepare Template File
Ensure `template.docx` exists in the project directory. This file should contain:
- Chapter placeholders: "Chapter 1 name", "Chapter 1 text", etc. for chapters 1-10
- Your desired book formatting and structure

## Usage

### 1. Start the Web Application
```bash
python app.py
```

### 2. Open Your Browser
Navigate to: `http://localhost:5000`

### 3. Fill Out the Form
- **Child Information**: Name, age, personality traits, interests
- **Genre Selection**: Choose from Sci-fi, Fantasy, Mystery, or Adventure
- **Plot Selection**: Choose from 2 options for your selected genre
- **Book Title**: Will auto-populate based on child's name
- **Training Documents** (Optional): Upload your writing samples (TXT, DOC, DOCX, PDF)

### 4. Generate Your Book
Click "Generate My Book!" and wait for processing (may take several minutes)

### 5. Download Your Book
Once complete, download the generated Word document

## Features

### Genre Options
- **Sci-fi**: Space adventures, time travel quests
- **Fantasy**: Magical kingdoms, dragon adventures
- **Mystery**: School detective stories, neighborhood secrets
- **Adventure**: Treasure hunts, wilderness survival

### Personalization
- Child's name integrated into story
- Age-appropriate content
- Personality traits influence character development
- Interests woven into plot elements

### Training Documents
Upload your own writing samples to influence the AI's:
- Writing style and tone
- Storytelling approach
- Character development
- Dialogue patterns

### Template System
Uses your `template.docx` file to:
- Maintain consistent formatting
- Apply your preferred styles
- Create professional-looking books
- Preserve document structure

## File Structure
```
chapter-book-generator/
├── app.py                  # Main Flask application
├── tools.py               # AI integration and document processing
├── server.py              # MCP server (optional)
├── template.docx          # Word template for books
├── templates/
│   └── index.html         # Web interface
├── uploads/               # Training documents storage
├── generated_books/       # Output directory (created automatically)
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Troubleshooting

### Common Issues

**"No module named 'anthropic'"**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`

**"API key not found"**
- Verify ANTHROPIC_API_KEY environment variable is set
- Check your Anthropic account has sufficient credits

**"Template file not found"**
- Ensure `template.docx` exists in project root
- Check file permissions

**Upload fails**
- Check file size (max 16MB)
- Verify file format (TXT, DOC, DOCX, PDF only)

**Book generation fails**
- Check internet connection
- Verify API key is valid
- Check Anthropic service status

### Getting Help
- Check console output for error messages
- Ensure all dependencies are installed
- Verify template.docx contains proper placeholders

## Advanced Configuration

### Customizing Genres/Plots
Edit the `GENRE_PLOTS` dictionary in `app.py` to add new genres or modify existing plots.

### Modifying AI Prompts
Update the prompt templates in `tools.py` to change how the AI generates content.

### Template Customization
Modify `template.docx` to change:
- Formatting styles
- Page layouts
- Header/footer content
- Chapter organization

## Security Notes
- API keys should never be committed to version control
- Use environment variables for sensitive configuration
- Uploaded documents are stored locally - implement cleanup as needed
- Consider adding authentication for production use