import sys
import os

# Add the project root to sys.path to allow importing from 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.sparse_encoder import encode_text

def test():
    text = "こんにちは、世界！"
    print(f"Encoding text: {text}")
    try:
        vector = encode_text(text)
        print("Success!")
        print(f"Vector size: {len(vector)}")
        print(f"Sample tokens: {list(vector.items())[:5]}")
    except Exception as e:
        print(f"Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
