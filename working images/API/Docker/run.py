import sys
import os
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

app = create_app()

if __name__ == "__main__":
    # IF RUNNING LOCALLY UNCOMMENT FIRST LINE COOMENT SECOND FOR DOCKER UNCOMMENT SECOND LINE COMMENT FIRST RUN BETTER THIS WAY NOT SURE WHY
    #app.run(port=5000) #for local running
    app.run(debug=True, host='0.0.0.0', port=5000) # for docker running
