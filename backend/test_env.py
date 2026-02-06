#!/usr/bin/env python3
"""
Quick test script to verify .env file is being read correctly
Run with: python test_env.py
"""
from app.core.config import settings

print("=== Environment Configuration Test ===\n")
print(f"Database URL: {settings.DATABASE_URL}")
print(f"LLM Farm Base URL: {settings.LLM_FARM_BASE_URL}")
print(f"LLM API Key: {'*' * 10 if settings.LLM_FARM_API_KEY else 'NOT SET'}")
print(f"Default Model: {settings.LLM_DEFAULT_MODEL}")
print(f"Default Max Tokens: {settings.LLM_DEFAULT_MAX_TOKENS}")
print(f"\nFull Endpoint: {settings.LLM_FARM_BASE_URL}/publishers/anthropic/models/{settings.LLM_DEFAULT_MODEL}:rawPredict")
print("\n=== Configuration Status ===")
if settings.LLM_FARM_API_KEY and settings.LLM_FARM_API_KEY != "your-api-key-here":
    print("✓ .env file loaded successfully")
else:
    print("⚠ Please update .env with real API key")
