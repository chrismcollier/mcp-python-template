#!/usr/bin/env python3
"""
Simple runner script for the Children's Chapter Book Generator
Handles basic setup checks and starts the Flask app
"""

import os
import sys

def check_environment():
    """Check if environment is properly set up"""
    print("🔍 Checking environment setup...")
    
    # Check if template exists
    if not os.path.exists('template.docx'):
        print("❌ template.docx not found!")
        print("   Please ensure template.docx exists in the project directory")
        return False
    
    # Check if API key is set
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("⚠️ ANTHROPIC_API_KEY environment variable not set")
        print("   The app will start but won't be able to generate books")
        print("   Set your API key: export ANTHROPIC_API_KEY=your-key-here")
    else:
        print("✅ ANTHROPIC_API_KEY found")
    
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('generated_books', exist_ok=True)
    print("✅ Required directories created/verified")
    
    return True

def main():
    """Main function"""
    print("🚀 Children's Chapter Book Generator")
    print("=" * 50)
    
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        return False
    
    print("\n✅ Environment check passed!")
    print("\nStarting Flask application...")
    print("Once started, open your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)