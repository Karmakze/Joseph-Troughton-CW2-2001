import sys
import os
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Add the API directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

app = create_app()

if __name__ == "__main__":
    #app.run(port=5000) #for local running
    app.run(debug=True, host='0.0.0.0', port=5000) # for docker running
