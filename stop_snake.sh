#!/bin/bash

# Check if the Snake executable exists
if [[ ! -f "./Snake.x86_64" ]]; then
  echo "Error: Snake.x86_64 not found in the current directory."
  exit 1
fi

# Number of instances to start
INSTANCE_COUNT=100000
PIDS=() # Array to store PIDs of the processes

echo "Starting $INSTANCE_COUNT instances of Snake.x86_64..."

# Loop to start instances
for ((i = 1; i <= INSTANCE_COUNT; i++)); do
  ./Snake.x86_64 &  # Start each instance in the background
  PID=$!            # Get the PID of the process
  PIDS+=($PID)      # Save the PID to the array
  echo "Started instance $i with PID $PID"
done

echo "All instances started."

# Wait for user input to kill the processes
read -p "Press Enter to terminate all instances..."

echo "Terminating all instances..."
for PID in "${PIDS[@]}"; do
  kill $PID && echo "Terminated PID $PID" || echo "Failed to terminate PID $PID"
done

echo "All instances terminated."

