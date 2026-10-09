#!/usr/bin/env bash
sudo podman rm -f eco 2>/dev/null
sudo podman container restore --tcp-established --import "${1:-$(ls -t backup/*.tar.gz | head -1)}"