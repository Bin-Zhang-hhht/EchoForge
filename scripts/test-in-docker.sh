#!/usr/bin/env sh
set -eu

SITE_OUTPUT_DIR="${SITE_OUTPUT_DIR:-./.cache/docker/site-dist}"
COLLECT_OUTPUT_DIR="${COLLECT_OUTPUT_DIR:-./.cache/docker/collected-items}"

# Git Bash rewrites Linux container paths unless conversion is disabled.
export MSYS_NO_PATHCONV="${MSYS_NO_PATHCONV:-1}"

mkdir -p "$SITE_OUTPUT_DIR" "$COLLECT_OUTPUT_DIR"
docker compose build site-build collector-test content-check
SITE_OUTPUT_DIR="$SITE_OUTPUT_DIR" docker compose run --rm site-build
COLLECT_OUTPUT_DIR="$COLLECT_OUTPUT_DIR" docker compose run --rm collector-test
docker compose run --rm content-check
docker compose run --rm workflow-lint

printf '%s\n' 'Docker site build, collector and M3 tests, content checks, and workflow lint passed.'
