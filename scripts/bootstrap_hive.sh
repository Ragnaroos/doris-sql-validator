#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JAR_DIR="${PROJECT_DIR}/docker/hive/jars"
JAR_PATH="${JAR_DIR}/postgresql-42.7.5.jar"
JAR_URL="https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.5/postgresql-42.7.5.jar"
EXPECTED_SHA256="69020b3bd20984543e817393f2e6c01a890ef2e37a77dd11d6d8508181d079ab"

mkdir -p "${JAR_DIR}"

if [[ -f "${JAR_PATH}" ]]; then
  actual_sha256="$(shasum -a 256 "${JAR_PATH}" | awk '{print $1}')"
  if [[ "${actual_sha256}" == "${EXPECTED_SHA256}" ]]; then
    echo "PostgreSQL JDBC driver already present and verified."
    exit 0
  fi
  echo "Existing JDBC driver checksum mismatch: ${actual_sha256}" >&2
  exit 1
fi

temporary_path="${JAR_PATH}.part"
trap 'rm -f "${temporary_path}"' EXIT
curl --fail --location --silent --show-error "${JAR_URL}" --output "${temporary_path}"

actual_sha256="$(shasum -a 256 "${temporary_path}" | awk '{print $1}')"
if [[ "${actual_sha256}" != "${EXPECTED_SHA256}" ]]; then
  echo "Downloaded JDBC driver checksum mismatch: ${actual_sha256}" >&2
  exit 1
fi

mv "${temporary_path}" "${JAR_PATH}"
echo "Downloaded and verified ${JAR_PATH}"

