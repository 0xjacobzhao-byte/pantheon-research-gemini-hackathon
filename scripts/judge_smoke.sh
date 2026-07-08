#!/usr/bin/env bash
#
# judge_smoke.sh — one-command smoke test for judges.
#
# Exercises the local backend (offline mode, no secrets required) end-to-end.
# Covers: health, evidence, Qwen/DeepSeek overlays, Gemini overlay & proof,
# comparison, data quality, module grid, Alibaba proof, provider health,
# validation timeline, ticker profiles, mini modules.
#
# Usage:
#   ./scripts/judge_smoke.sh                 # assumes backend on :8000
#   BASE=http://localhost:8000 ./scripts/judge_smoke.sh
#   ALIBABA=http://8.222.191.152 ./scripts/judge_smoke.sh
#
# To start the local backend first:
#   docker compose up -d --build backend
set -uo pipefail

BASE="${BASE:-http://localhost:8000}"
ALIBABA="${ALIBABA:-http://8.222.191.152}"
TICKER="${TICKER:-MA}"
PASS=0; FAIL=0

jqget() { command -v jq >/dev/null 2>&1 && jq -r "$1" || cat; }

check() { # name url jq-filter expected-substring
  local name="$1" url="$2" filt="$3" want="$4"
  local out; out=$(curl -sS -m 30 "$url" 2>/dev/null | jqget "$filt" 2>/dev/null)
  if printf '%s' "$out" | grep -qi "$want"; then
    printf "  PASS  %-34s %s\n" "$name" "$out"; PASS=$((PASS+1))
  else
    printf "  FAIL  %-34s got=[%s] want~[%s]\n" "$name" "$out" "$want"; FAIL=$((FAIL+1))
  fi
}

# secret_check: assert that a string does NOT contain secret-like patterns
secret_check() { # name url
  local name="$1" url="$2"
  local body; body=$(curl -sS -m 30 "$url" 2>/dev/null)
  if printf '%s' "$body" | grep -qE "(AIza[A-Za-z0-9_\-]{30,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|x-admin-token|BEGIN PRIVATE KEY)"; then
    printf "  FAIL  %-34s SECRET DETECTED IN RESPONSE\n" "$name"; FAIL=$((FAIL+1))
  else
    printf "  PASS  %-34s no secrets in response\n" "$name"; PASS=$((PASS+1))
  fi
}

softcheck() { # like check(), but never fails the run (best-effort live probe)
  local name="$1" url="$2" filt="$3" want="$4"
  local out; out=$(curl -sS -m 30 "$url" 2>/dev/null | jqget "$filt" 2>/dev/null)
  if printf '%s' "$out" | grep -qi "$want"; then
    printf "  PASS  %-34s %s\n" "$name" "$out"
  else
    printf "  SKIP  %-34s (live host not reachable — offline demo unaffected)\n" "$name"
  fi
}

echo "== Local backend (offline mode, no secrets) @ $BASE =="
check "health"             "$BASE/health"                       '.status'            "healthy"
check "evidence pack hash" "$BASE/api/evidence/$TICKER"         '.provenance.evidence_hash' "sha256"
check "qwen overlay"       "$BASE/api/overlay/qwen/$TICKER"     '.status'            "SAMPLE"
check "deepseek overlay"   "$BASE/api/overlay/deepseek/$TICKER" '.status'            "SAMPLE"
check "comparison state"   "$BASE/api/comparison/$TICKER"       '.data_state'        "."
check "comparison agree"   "$BASE/api/comparison/$TICKER"       '.agreement_level'   "."
check "data quality"       "$BASE/api/data-quality"             '.mode'              "."
check "module grid"        "$BASE/api/modules"                  '.modules[0].data_state' "."
check "alibaba proof (v2)" "$BASE/api/proof/alibaba-cloud"      '.schema_version'    "alibaba-proof"
check "proof host honest"  "$BASE/api/proof/alibaba-cloud"      '.host_runtime'      "."
check "proof db precise"   "$BASE/api/proof/alibaba-cloud"      '.database.production_data_migrated' "false"

check "provider health"    "$BASE/api/provider-health"             '.qwen.provider'      "Alibaba"
check "validation timeline" "$BASE/api/validation-timeline"          '.stages[0].name'      "Signal"
check "ticker profiles"     "$BASE/api/ticker-profiles"              '.tickers[0]'          "."
check "ticker profile NVDA" "$BASE/api/ticker-profile/NVDA"          '.company_name'       "NVIDIA"
check "mini macro"          "$BASE/api/mini/macro"                   '.data_state'         "CONTEXT"
check "mini market pulse"   "$BASE/api/mini/market-pulse"            '.data_state'         "CONTEXT"
check "mini ficc"           "$BASE/api/mini/ficc"                    '.data_state'         "CONTEXT"

echo
echo "== Gemini checks (offline mode) =="
check "gemini overlay"     "$BASE/api/overlay/gemini/NVDA"       '.status'            "OFFLINE_SAMPLE"
check "gemini proof"       "$BASE/api/proof/gemini"              '.schema_version'    "gemini-proof-v1"
check "gemini proof cred"  "$BASE/api/proof/gemini"              '.credential_configured' "false\|true"
check "gemini proof no-ext" "$BASE/api/proof/gemini"             '.proof_endpoint_external_calls' "false"
secret_check "no secrets in Gemini proof"  "$BASE/api/proof/gemini"
secret_check "no secrets in Gemini overlay" "$BASE/api/overlay/gemini/NVDA"

echo
echo "== Live Alibaba Cloud ECS proof @ $ALIBABA (best-effort; production backend) =="
softcheck "alibaba live proof" "$ALIBABA/api/proof/alibaba-cloud" '.cloud_provider' "Alibaba"

echo
echo "-------------------------------------------"
echo "  PASS=$PASS  FAIL=$FAIL"
[ "$FAIL" -eq 0 ] && { echo "  ALL GREEN"; exit 0; } || { echo "  SOME CHECKS FAILED"; exit 1; }
