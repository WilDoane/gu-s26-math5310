mkdir -p workspace

if ! podman machine inspect --format '{{.State}}' 2>/dev/null | grep -q running; then
  podman machine start
fi

podman build -t dl-cpu -f Dockerfile .

# podman run --rm \
#   -v "$(pwd -W 2>/dev/null || pwd)/extract_all.py:/app/extract_all.py:ro" \
#   -v "$(pwd -W 2>/dev/null || pwd)/docling-models:/models" \
#   docling-cpu \
#   /models
