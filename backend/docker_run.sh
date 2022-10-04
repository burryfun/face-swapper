xhost +local:docker
docker run -it -p 5000:5000 --rm --gpus all --name faceswap_cv -v $(pwd)/test_videos:/usr/src/app/test_videos -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY faceswap_cv
