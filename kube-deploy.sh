#!/bin/bash
set -e

NAMESPACE=lowry

# Enable ingress controller (minikube/local)
kubectl get ns ingress-nginx || kubectl create ns ingress-nginx
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

# Install cert-manager
kubectl get ns cert-manager || kubectl create ns cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml

# Create namespace if not exists
kubectl get ns $NAMESPACE || kubectl create ns $NAMESPACE

# Apply secrets and config
kubectl apply -f k8s/secrets.yml -n $NAMESPACE
kubectl apply -f k8s/config.yml -n $NAMESPACE

# Apply core services
kubectl apply -f k8s/db.yml -n $NAMESPACE
kubectl apply -f k8s/redis.yml -n $NAMESPACE
kubectl apply -f k8s/minio.yml -n $NAMESPACE

# Wait for core pods
echo "Waiting for DB, Redis, MinIO..."
kubectl wait --for=condition=Ready pod -l app=lowry-db -n $NAMESPACE --timeout=120s
kubectl wait --for=condition=Ready pod -l app=lowry-redis -n $NAMESPACE --timeout=120s
kubectl wait --for=condition=Ready pod -l app=lowry-minio -n $NAMESPACE --timeout=120s

# Run migrations
kubectl apply -f k8s/migration.yml -n $NAMESPACE
kubectl wait --for=condition=Complete job/lowry-migration -n $NAMESPACE --timeout=180s

# Apply worker, API, frontend
kubectl apply -f k8s/worker.yml -n $NAMESPACE
kubectl apply -f k8s/api.yml -n $NAMESPACE
kubectl apply -f k8s/frontend.yml -n $NAMESPACE

# Apply Ingresses
kubectl apply -f k8s/lowry-ingress.yml -n $NAMESPACE
kubectl apply -f k8s/minio-ingress.yml -n $NAMESPACE

# Apply ClusterIssuer
kubectl apply -f k8s/clusterissuer.yml

# Apply Certificate
kubectl apply -f k8s/certificate.yml -n $NAMESPACE

# Wait for all pods
echo "Waiting for API, Celery, Frontend..."
kubectl wait --for=condition=Ready pod -l app=lowry-api -n $NAMESPACE --timeout=120s
kubectl wait --for=condition=Ready pod -l app=lowry-celery -n $NAMESPACE --timeout=120s
kubectl wait --for=condition=Ready pod -l app=lowry-frontend -n $NAMESPACE --timeout=120s

echo "Waiting for TLS certificate..."
kubectl wait --for=condition=Ready certificate/lowry-tls -n $NAMESPACE --timeout=300s

echo "✅ Deployment complete! Access your services via localhost."
