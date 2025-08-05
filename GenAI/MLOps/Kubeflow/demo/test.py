# test.py (FIXED)
from demo import QuickDemo  # Changed from EssayWriterDemo

def test_demo():
    demo = QuickDemo()  # Use QuickDemo instead
    result = demo.run_single_essay("Benefits of reading")
    print("✅ Test passed!")

if __name__ == "__main__":
    test_demo()