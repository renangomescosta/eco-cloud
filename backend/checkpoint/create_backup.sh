#!/usr/bin/env bash
mkdir -p backup
sudo podman container checkpoint app --leave-running --export backup/cp-$(date +%Y%m%d-%H%M%S).tar.gz