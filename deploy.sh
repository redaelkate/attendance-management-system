#!/bin/bash

# Start ngrok for port 5173 with the provided authtoken
if ! command -v ngrok &> /dev/null; then
    echo "Error: ngrok is not installed. Please install ngrok and try again."
    exit 1
fi

source myenv/bin/activate

# Run the Python app in detached mode
python app.py &

# Navigate to the frontend directory and run npm in detached mode
cd frontend && npm run dev &

# Start ngrok in detached mode
ngrok http --url=flexible-fine-salmon.ngrok-free.app 5173 &

# Check if ngrok started successfully
if [ $? -ne 0 ]; then
    echo "Error: Failed to start ngrok. Please check your configuration."
    exit 1
fi