"""
Test OpenRouter Connection
Quick script to verify OpenRouter API is working
"""
import os
from openai import OpenAI

# Load API key
api_key = "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"

print("🔍 Testing OpenRouter Connection...")
print(f"API Key: {api_key[:20]}...{api_key[-10:]}")
print()

try:
    # Initialize OpenRouter client (uses OpenAI SDK)
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Prometheus"
        }
    )
    
    print("📡 Sending test request to OpenRouter...")
    
    # Make a simple test request
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",  # Cheapest model for testing
        messages=[
            {"role": "user", "content": "Say 'OpenRouter está funcionando!' in Portuguese"}
        ],
        max_tokens=50
    )
    
    print("✅ OpenRouter Connected Successfully!")
    print()
    print("📝 Response:", response.choices[0].message.content)
    print()
    print(f"🔢 Tokens Used: {response.usage.total_tokens}")
    print(f"💰 Model: {response.model}")
    print()
    print("🎉 OpenRouter integration is working!")
    
except Exception as e:
    print("❌ Error connecting to OpenRouter:")
    print(f"   {type(e).__name__}: {e}")
    print()
    print("💡 Troubleshooting:")
    print("   1. Check if API key is correct")
    print("   2. Verify internet connection")
    print("   3. Check OpenRouter status at https://openrouter.ai/status")
