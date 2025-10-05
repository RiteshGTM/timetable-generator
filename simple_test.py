#!/usr/bin/env python3
"""
Simple test to verify the Flask app is working
"""

import requests
import time

def test_app():
    """Test if the Flask app is running"""
    print("Testing Flask app...")
    
    # Wait a moment for the app to start
    time.sleep(2)
    
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code == 200:
            print("SUCCESS: Flask app is running!")
            print(f"Response length: {len(response.text)} characters")
            return True
        else:
            print(f"FAIL: Flask app returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("FAIL: Cannot connect to Flask app. Make sure it's running.")
        return False
    except Exception as e:
        print(f"FAIL: Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_app()

