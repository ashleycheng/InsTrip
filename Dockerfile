FROM ubuntu:20.04

WORKDIR /usr/src/app

EXPOSE 8000

# Volumes
VOLUME /usr/src/app/log
VOLUME /usr/src/app/media
VOLUME /usr/src/app/assets

# Install python packages
RUN apt-get update \
  && apt-get install -y git \
  && apt-get install -y python3.8 python3.8-dev python3-pip \
  && apt-get clean autoclean \
  && rm -rf /var/lib/{apt,dpkg,cache,log}/

RUN ln -s /usr/bin/python3.8 /usr/bin/python

# set Python 3.8 as default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# upgade pip to the latest version
RUN python3.8 -m pip install --upgrade pip

# Install Node.js and npm
RUN apt-get install curl -y
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash
RUN apt-get install -y nodejs
    
COPY . .

# Copy docker-entrypoint.sh
RUN mv ./docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

RUN python3.8 -m pip install --upgrade pip setuptools wheel
RUN pip3 install --upgrade pip setuptools uwsgi
RUN pip install --no-cache-dir -r requirements.txt

# Install npm packges
RUN npm install -g npm
RUN npm install

ENTRYPOINT [ "docker-entrypoint.sh" ]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]
