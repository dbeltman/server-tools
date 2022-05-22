registryurl="dockerhub.evendaanbellen.nl"
owner="dockerdaan"
repo="r510-denoiser"
tag="develop"

docker build -t $registryurl/$owner/$repo:$tag -f Dockerfile .
#docker push $registryurl/$owner/$repo:$tag
docker run --rm --name R510-DenoiserV2-developtmp --network apps --device /dev/ipmi0:/dev/ipmi0 $registryurl/$owner/$repo:$tag
