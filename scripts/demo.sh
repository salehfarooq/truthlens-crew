#!/usr/bin/env bash
set -euo pipefail

truthlens verify "Pakistan gained independence in 1947."
truthlens benchmark data/sample/claims.csv

