
#################################################################### 


FROM python:3.9



# apt 속도 향상
#RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list
#RUN sed -i 's/security.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

RUN pip install --upgrade pip

RUN mkdir -p /root/knowwhresoft/EventServer
WORKDIR /root/knowwheresoft/EventServer

## Install packages
COPY ../../Users/kyj/Desktop/docker/requirements.txt ./
RUN pip install -r requirements.txt

## Copy all src files
COPY ../../Users/kyj/Desktop/docker .

## Run the application on the port 8080
EXPOSE 7000

# gunicorn 배포 명령어
# CMD ["gunicorn", "--bind", "허용하는 IP:열어줄 포트", "project.wsgi:application"]
CMD ["gunicorn", "--bind", "0.0.0.0:7000", "stock.wsgi:application"]

########################################################################


ARG DEBIAN_FRONTEND=noninteractive
RUN apt update -y 
RUN apt -o Acquire::Retries=3 -qy install net-tools
RUN apt -o Acquire::Retries=3 -y install iputils-ping
RUN apt -o Acquire::Retries=3 -y install firewalld
RUN apt -o Acquire::Retries=3 -y install vim 
RUN apt -o Acquire::Retries=3 -y install git
RUN apt -o Acquire::Retries=3 -y install unzip
RUN apt -o Acquire::Retries=3 -y install wget
RUN apt -o Acquire::Retries=3 -y install curl 
RUN apt -o Acquire::Retries=3 -y install lshw
RUN apt -o Acquire::Retries=3 -y install tcpdump
RUN apt -o Acquire::Retries=3 -y install lsof
RUN apt -o Acquire::Retries=3 -y install jq
RUN apt -o Acquire::Retries=3 -y install openssl
RUN apt -o Acquire::Retries=3 -y install libssl-dev
RUN apt -o Acquire::Retries=3 -y install uwf
RUN apt -o Acquire::Retries=3 -y install openssh-server
RUN apt -o Acquire::Retries=3 -y install build-essential cmake git pkg-config dkms


############################################# 한글입력 가능

RUN echo 'export LANG=ko_KR.utf8' >> /root/.bashrc
RUN echo 'export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python' >> /root/.bashrc
RUN echo "alias ll='ls -al --color=auto'" >> /root/.bashrc

# -------------------------------------------------
# ssh 설정
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config



# openssh server 실행
RUN service ssh start 