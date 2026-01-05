mkdir -p workspace

USER_ID=$(id -u)
GROUP_ID=$(id -g)

if ! podman machine inspect --format '{{.State}}' 2>/dev/null | grep -q running; then
  podman machine start
fi

podman run --rm -it \
  --userns=keep-id \
  --user "${USER_ID}:${GROUP_ID}" \
  -p8888:8888 \
  -v "$(pwd -W 2>/dev/null || pwd)/workspace:/workspace:rw,z" dl-cpu

# CTRL-C to exit
