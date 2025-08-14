#!/bin/bash

# kurbeScript.sh
# Script to set up and verify a local Kubernetes cluster using Minikube

echo "=== Kubernetes Local Setup Script ==="

# 1️⃣ Check if Minikube is installed
if ! command -v minikube &> /dev/null
then
    echo "Minikube not found. Installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
        sudo install minikube-linux-amd64 /usr/local/bin/minikube
        rm minikube-linux-amd64
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install minikube
    else
        echo "Unsupported OS. Please install Minikube manually: https://minikube.sigs.k8s.io/docs/start/"
        exit 1
    fi
else
    echo "✅ Minikube is already installed."
fi

# 2️⃣ Start Minikube cluster
echo "Starting Minikube cluster..."
minikube start

# 3️⃣ Verify cluster status
echo "Verifying cluster..."
kubectl cluster-info

# 4️⃣ List available pods in all namespaces
echo "Retrieving available pods..."
kubectl get pods --all-namespaces

echo "=== Kubernetes setup complete! ==="
