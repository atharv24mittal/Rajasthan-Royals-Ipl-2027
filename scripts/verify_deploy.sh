#!/usr/bin/env bash
# Run against the REAL deployment: bash scripts/verify_deploy.sh https://your-project.vercel.app user pass
URL="${1:?url}"; U="${2:?user}"; P="${3:?pass}"; f=0
chk(){ if [ "$2" = "$3" ]; then echo "PASS $1 ($2)"; else echo "FAIL $1 (got $2, want $3)"; f=1; fi; }
chk "no credentials -> 401" "$(curl -s -o /dev/null -w '%{http_code}' "$URL/")" 401
chk "wrong credentials -> 401" "$(curl -s -o /dev/null -w '%{http_code}' -u "$U:wrong" "$URL/")" 401
chk "data file not public without auth" "$(curl -s -o /dev/null -w '%{http_code}' "$URL/data/stage2.js")" 401
chk "valid credentials -> 200" "$(curl -s -o /dev/null -w '%{http_code}' -u "$U:$P" "$URL/")" 200
curl -s -D - -o /dev/null -u "$U:$P" "$URL/" | grep -qi 'x-robots-tag: noindex' && echo "PASS noindex header" || { echo "FAIL noindex header"; f=1; }
curl -s -o /dev/null -w '%{http_code}\n' -u "$U:$P" "$URL/raw/ball_by_ball.csv" | grep -q 200 && { echo "FAIL raw data reachable"; f=1; } || echo "PASS no raw dataset path"
exit $f
