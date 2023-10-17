FROM --platform=linux/amd64 ubuntu:22.04

RUN apt-get update && apt-get install -y software-properties-common git python3-pip \
    && pip3 install torch==1.11.0+cpu torchvision==0.12.0+cpu -f https://download.pytorch.org/whl/torch_stable.html \
    && pip3 install evadb faiss-cpu sentence-transformers find-libpython \
    && pip3 uninstall evadb -y 
