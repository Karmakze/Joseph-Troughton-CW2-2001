import sys
import os

# Add project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
print(sys.path)

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
