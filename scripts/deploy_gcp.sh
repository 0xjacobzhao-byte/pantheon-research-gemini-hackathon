#!/usr/bin/env bash
#
# deploy_gcp.sh - Deploy Pantheon Research Gemini backend to Google Cloud Run.
#
# Prerequisites:
#   gcloud CLI installed and authenticated
#   GCP project set (gcloud config set project <PROJECT_ID>)
#   Docker installed
#
# Usage:
#   ./scripts/deploy_gcp.sh
#   GCP_REGION=us-central1 ./scripts/deploy_gcp.sh
#   GEMINI_API_KEY=AIza... ./scripts/deploy_gcp.sh
#
set -euo pipefail

GCP_PROJECT="${GCP_PROJECT:-$(gcloud config get-value project 2>/dev/null)}"
GCP_REGION="${GCP_REGION:-asia-southeast1}"
SERVICE_NAME="${SERVICE_NAME:-pantheon-gemini}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IMAGE="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${SERVICE_NAME}/${SERVICE_NAME}:latest"

echo "== Pantheon Research Gemini Cloud Run Deploy =="
echo "  Project:  ${GCP_PROJECT}"
echo "  Region:   ${GCP_REGION}"
echo "  Service:  ${SERVICE_NAME}"
echo "  Image:    ${IMAGE}"
echo ""

# Preflight
if [ -z "$GCP_PROJECT" ] || [ "$GCP_PROJECT" = "(unset)" ]; then
    echo "ERROR: No GCP project. Run: gcloud auth login && gcloud config set project <PROJECT_ID>"
    exit 1
fi

if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null | head -1 | grep -q "@"; then
    echo "ERROR: No active gcloud account. Run: gcloud auth login"
    exit 1
fi

# Enable APIs
echo "==> Enabling APIs..."
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com \
    cloudbuild.googleapis.com \
    --project="${GCP_PROJECT}" 2>/dev/null || true

# Artifact Registry
echo "==> Ensuring Artifact Registry..."
gcloud artifacts repositories describe "${SERVICE_NAME}" \
    --location="${GCP_REGION}" --project="${GCP_PROJECT}" 2>/dev/null || \
gcloud artifacts repositories create "${SERVICE_NAME}" \
    --repository-format=docker --location="${GCP_REGION}" \
    --project="${GCP_PROJECT}" \
    --description="Pantheon Research Gemini backend"

# Docker auth
echo "==> Configuring Docker auth..."
gcloud auth configure-docker "${GCP_REGION}-docker.pkg.dev" --quiet

# Build & push (context = repo root, uses root Dockerfile)
echo "==> Building image..."
cd "${REPO_ROOT}"
docker build -t "${IMAGE}" -f Dockerfile .
echo "==> Pushing image..."
docker push "${IMAGE}"

# Secret (optional)
SECRET_NAME="gemini-api-key"
if [ -n "${GEMINI_API_KEY:-}" ]; then
    echo "==> Setting Gemini API key secret..."
    echo -n "${GEMINI_API_KEY}" | \
        gcloud secrets create "${SECRET_NAME}" \
            --project="${GCP_PROJECT}" --data-file=- \
            --replication-policy=automatic 2>/dev/null || \
    echo -n "${GEMINI_API_KEY}" | \
        gcloud secrets versions add "${SECRET_NAME}" \
            --project="${GCP_PROJECT}" --data-file=-
fi

# Deploy
echo "==> Deploying to Cloud Run..."
DEMO_MODE_VAL=offline
SECRET_FLAGS=""
if gcloud secrets describe "${SECRET_NAME}" --project="${GCP_PROJECT}" 2>/dev/null | grep -q "name:"; then
    SECRET_FLAGS="--set-secrets=GEMINI_API_KEY=${SECRET_NAME}:latest"
    DEMO_MODE_VAL=live
fi

gcloud run deploy ${SERVICE_NAME} \
    --image="${IMAGE}" \
    --region="${GCP_REGION}" \
    --project="${GCP_PROJECT}" \
    --platform=managed \
    --allow-unauthenticated \
    --memory=512Mi \
    --cpu=1 \
    --min-instances=0 \
    --max-instances=3 \
    --timeout=60 \
    --port=8080 \
    --set-env-vars="DEMO_MODE=${DEMO_MODE_VAL},GOOGLE_CLOUD_REGION=${GCP_REGION},GOOGLE_CLOUD_PROJECT=${GCP_PROJECT}" \
    ${SECRET_FLAGS}

# Report
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" \
    --region="${GCP_REGION}" --project="${GCP_PROJECT}" --format="value(status.url)")
echo ""
echo "== Deployed ==
echo "  URL:              ${SERVICE_URL}"
echo "  Health:           ${SERVICE_URL}/health"
echo "  Gemini proof:     ${SERVICE_URL}/api/proof/gemini"
echo "  GCP proof:        ${SERVICE_URL}/api/proof/gcp"
echo "  Gemini overlay:   ${SERVICE_URL}/api/overlay/gemini/NVDA"
echo "  API docs:         ${SERVICE_URL}/docs"
echo ""
echo "Verify:"
echo "  curl -s ${SERVICE_URL}/health | jq"
echo "  curl -s ${SERVICE_URL}/api/proof/gemini | jq"
echo "  curl -s ${SERVICE_URL}/api/proof/gcp | jq"
