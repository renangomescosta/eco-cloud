#!/usr/bin/env bash
mkdir -p backup
sudo podman container checkpoint eco --leave-running --tcp-established --export "backup/cp-$(date +%Y%m%d-%H%M%S).tar.gz"