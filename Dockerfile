FROM ubuntu
RUN apt update -y && apt upgrade -y && apt install -y python3 python3-pip
RUN pip3 install numpy tensorflow tensorflow_datasets imap_tools
RUN mkdir /NN
ADD https://raw.githubusercontent.com/CNC5/refactored-octo-engine/main/filter_script.py \ /NN/
