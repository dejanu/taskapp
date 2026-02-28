#!/bin/bash

# Bash script to create 5 tasks incrementally using curl
for i in {1..5}
do
  curl -X POST http://localhost:8000/tasks \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Task $i\"}"
done
