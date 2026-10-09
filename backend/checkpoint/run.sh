#!/usr/bin/env bash
sudo podman build -t eco-cloud . ; sudo podman rm -f eco 2>/dev/null
sudo podman run -d --name eco -p 3000:3000 eco-cloud