ARG PYTORCH="1.11.0"
ARG CUDA="11.3"
ARG CUDNN="8"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

WORKDIR /usr/src/app

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

RUN apt-get update && apt-get install -y nano ffmpeg libsm6 libxext6

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "--app", "api/main.py", "run", "--host=0.0.0.0", "--port=5000"]