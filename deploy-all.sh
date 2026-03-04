#!/bin/bash
# deploy-all.sh
# Run this script to deploy everything at once!
# Usage: bash deploy-all.sh

echo "🚀 Deploying Hello App to Kubernetes..."
echo ""

# Step 1: Create namespace
echo "📦 Step 1/6 — Creating namespace..."
kubectl apply -f namespace.yaml
echo ""

# Step 2: ConfigMap
echo "📝 Step 2/6 — Applying ConfigMap (settings)..."
kubectl apply -f configmap.yaml
echo ""

# Step 3: Secret
echo "🔒 Step 3/6 — Applying Secrets (passwords)..."
kubectl apply -f secret.yaml
echo ""

# Step 4: Deployment
echo "🏗️  Step 4/6 — Deploying the app (3 replicas)..."
kubectl apply -f deployment.yaml
echo ""

# Step 5: Service
echo "🛣️  Step 5/6 — Creating Service (internal network road)..."
kubectl apply -f service.yaml
echo ""

# Step 6: Ingress
echo "🚪 Step 6/6 — Setting up Ingress (public address)..."
kubectl apply -f ingress.yaml
echo ""

# Step 7: HPA
echo "✨ Bonus — Enabling auto-scaling (HPA)..."
kubectl apply -f hpa.yaml
echo ""

# Wait for pods to be ready
echo "⏳ Waiting for pods to be ready..."
kubectl rollout status deployment/hello-app -n my-app
echo ""

# Show final status
echo "✅ Deployment complete! Here's what's running:"
echo ""
echo "--- PODS ---"
kubectl get pods -n my-app
echo ""
echo "--- SERVICES ---"
kubectl get services -n my-app
echo ""
echo "--- INGRESS ---"
kubectl get ingress -n my-app
echo ""
echo "🎉 Your app should be live at: http://hello.myapp.com"
echo "   (Make sure DNS points hello.myapp.com to your cluster IP)"
