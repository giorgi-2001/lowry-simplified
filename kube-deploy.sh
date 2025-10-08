#!/bin/bash
set -e

NAMESPACE=lowry

# 0️⃣ Enable ingress controller (minikube/local)
kubectl get ns ingress-nginx || kubectl create ns ingress-nginx
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml

# 1️⃣ Create namespace if not exists
kubectl get ns $NAMESPACE || kubectl create ns $NAMESPACE

# 2️⃣ Apply secrets and config
kubectl apply -f k8s/secrets.yml -n $NAMESPACE
kubectl apply -f k8s/config.yml -n $NAMESPACE

# 3️⃣ Apply core services
kubectl apply -f k8s/db.yml -n $NAMESPACE
kubectl apply -f k8s/redis.yml -n $NAMESPACE
kubectl apply -f k8s/minio.yml -n $NAMESPACE

# 4️⃣ Wait for core pods
echo "Waiting for DB, Redis, MinIO..."
kubectl wait --for=condition=Ready pod -l app=lowry-db -n $NAMESPACE --timeout=120s
kubectl wait --for=condition=Ready pod -l app=lowry-redis -n $NAMESPACE --timeout=120s
kubectl wait --for=condition=Ready pod -l app=lowry-minio -n $NAMESPACE --timeout=120s

# 5️⃣ Run migrations
kubectl apply -f k8s/migration.yml -n $NAMESPACE
kubectl wait --for=condition=Complete job/lowry-migration -n $NAMESPACE --timeout=120s

# 6️⃣ Apply worker, API, frontend
kubectl apply -f k8s/worker.yml -n $NAMESPACE
kubectl apply -f k8s/api.yml -n $NAMESPACE
kubectl apply -f k8s/frontend.yml -n $NAMESPACE

# 7️⃣ Apply Ingresses
kubectl apply -f k8s/lowry-ingress.yml -n $NAMESPACE
kubectl apply -f k8s/minio-ingress.yml -n $NAMESPACE

# 8️⃣ Wait for all pods
echo "Waiting for API, Celery, Frontend..."
kubectl wait --for=condition=Ready pod -l app=lowry-api -n $NAMESPACE --timeout=120s
kubectl wait --for=condition=Ready pod -l app=lowry-celery -n $NAMESPACE --timeout=120s
kubectl wait --for=condition=Ready pod -l app=lowry-frontend -n $NAMESPACE --timeout=120s

echo "✅ Deployment complete! Access your services via localhost."
