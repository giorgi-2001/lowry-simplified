#!/bin/sh
set -e

# If index.html exists, substitute placeholders
INDEX_FILE="/usr/share/nginx/html/index.html"

if [ -f "$INDEX_FILE" ]; then
  # Provide defaults if not set
  : "${VITE_API_BASE:=/api}"
  : "${VITE_MINIO_PREFIX:=/minio}"

  # Using envsubst to replace placeholders in index.html
  # Placeholders must look like: __VITE_API_BASE__ and __VITE_MINIO_PREFIX__
  export VITE_API_BASE VITE_MINIO_PREFIX

  # Create a temp file and substitute
  envsubst '${VITE_API_BASE} ${VITE_MINIO_PREFIX}' < "$INDEX_FILE" > "${INDEX_FILE}.tmp" && \
    mv "${INDEX_FILE}.tmp" "$INDEX_FILE"
fi

# Start nginx (CMD will execute afterwards, but keep entrypoint safe)
exec "$@"