#!/usr/bin/env python3
"""
Simple startup script for the AI Chatbot
"""
import uvicorn
import os

if __name__ == "__main__":
    print("🚀 Starting AI Chatbot Server...")
    print("📱 Open your browser and go to: http://localhost:8000")
    print("🔧 Make sure your .env file is configured with GROQ_API_KEY")
    print("-" * 50)
    
    # Start the FastAPI server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
