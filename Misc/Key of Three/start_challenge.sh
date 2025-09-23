#!/bin/bash

# Build and run the CTF challenge
echo "🚀 Building CTF Challenge..."
docker build -t ctf-chmod-challenge .

echo "📦 Starting challenge in background..."
docker run -d -p 1337:1337 --name running-ctf-challenge ctf-chmod-challenge

echo "✅ Challenge is running!"
echo "🌐 Connect with: nc localhost 1337"
echo "📋 Check logs with: docker logs running-ctf-challenge"
echo "🛑 Stop with: docker stop running-ctf-challenge && docker rm running-ctf-challenge"