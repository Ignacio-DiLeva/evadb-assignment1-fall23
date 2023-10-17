FROM --platform=linux/amd64 ubuntu:22.04

WORKDIR /home/root

COPY ./docs/requirements.txt ./requirements.txt

RUN apt-get update && apt-get install -y software-properties-common git python3-pip \
    && pip3 install evadb \
    && pip3 install -r /home/root/requirements.txt \
    && rm /home/root/requirements.txt \
    && pip3 install torch==1.11.0+cpu torchvision==0.12.0+cpu -f https://download.pytorch.org/whl/torch_stable.html \
    && pip3 install faiss-cpu pandas sentence-transformers find-libpython \
    && pip3 uninstall evadb -y 
