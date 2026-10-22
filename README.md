# aks-project

Containerized Python (Flask) application deployed to **Azure Kubernetes Service (AKS)** through a fully automated **GitHub Actions** pipeline, using **OIDC authentication** (no stored Azure credentials).

## Architecture

```
GitHub (push to main)
   │
   ▼
GitHub Actions ──OIDC──► Azure AD (federated credentials)
   │
   ├─► CI: install dependencies + Docker build validation (PRs)
   ├─► Build & push image ──► Azure Container Registry (ACR)
   └─► Deploy ──kubectl──► AKS cluster
                              ├─ Deployment (2 replicas, rolling update)
                              └─ Service (Azure LoadBalancer, port 80 → 5000)
```

## Highlights

- **Passwordless CI/CD**: GitHub Actions authenticates to Azure with OpenID Connect (federated identity), no client secret stored in the repository.
- **Zero-downtime deployments**: `RollingUpdate` strategy with `maxSurge: 1` and `maxUnavailable: 0`.
- **Self-healing**: liveness and readiness probes on the `/healthz` endpoint.
- **High availability**: 2 replicas behind an Azure Load Balancer.
- **Pull request validation**: every PR builds the Docker image before merge.
- **AKS authentication** with `kubelogin` (Azure AD integrated cluster).

## Project structure

```
aks-project/
├── app.py                         # Flask application (/ and /healthz)
├── requirements.txt
├── Dockerfile                     # python:3.10-slim image
├── k8s/
│   ├── deployment.yml             # Deployment, probes, rolling update
│   └── service.yml                # LoadBalancer service
└── .github/workflows/
    └── deploy-kubernetes.yml      # CI → build & push to ACR → deploy to AKS
```

## Pipeline

| Trigger | Jobs |
|---|---|
| Pull request | Install dependencies, Docker build validation |
| Push to `main` | CI → build & push image to ACR → deploy manifests to AKS |

### Required repository variables

| Variable | Description |
|---|---|
| `CLIENT_ID` | Azure AD application (client) ID with federated credentials |
| `TENANT_ID` | Azure AD tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID |
| `ACR_NAME` | Azure Container Registry name |

## Run locally

```bash
pip install -r requirements.txt
python app.py
curl http://localhost:5000/healthz   # healthy
```

With Docker:

```bash
docker build -t k8s-test-app .
docker run -p 5000:5000 k8s-test-app
```

## Tech stack

Azure (AKS, ACR, Azure AD / OIDC) · Kubernetes · Docker · GitHub Actions · Python / Flask

## Author

**Hermann Djoko** — DevOps & Cloud Engineer (AWS / Azure)
[GitHub](https://github.com/HermannDj) · [LinkedIn](https://linkedin.com/in/hermanndjoko) · harnaud.djoko@gmail.com
