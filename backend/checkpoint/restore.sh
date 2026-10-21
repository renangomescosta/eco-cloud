#!/usr/bin/env bash
sudo podman load -i ~/backup/app-20261021-125647.tar.gz
sudo podman container restore --import ~/backup/cp-XXXXXXXX-XXXXXX.tar.gz