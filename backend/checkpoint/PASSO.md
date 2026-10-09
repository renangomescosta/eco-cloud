docker run --privileged -it ubuntu bash (HOST)

sudo docker cp backup/cp-20261009-192406.tar.gz elastic_gauss:/ (HOST)
apt update && apt install podman fuse-overlayfs -y
2
135
32
docker save -o eco-cloud.tar eco-cloud (HOST)
sudo docker cp eco-cloud.tar elastic_gauss:/ (HOST)
podman load -i /eco-cloud.tar
podman tag docker.io/library/eco-cloud:latest localhost/eco-cloud:latest


IMPEDITIVO: DOCKER EM CIMA DE DOCKER DAR RUIM.