FROM debian:latest
MAINTAINER SaDev Four lokikiller@126.com

#install pip nginx
COPY ./misc/nginx_signing.key /var/www/app/nginx_signing.key
RUN apt-key add /var/www/app/nginx_signing.key
RUN echo "deb http://nginx.org/packages/debian/ jessie nginx" >> /etc/apt/sources.list
RUN echo "deb-src http://nginx.org/packages/debian/ jessie nginx" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y nginx \
    build-essential \
    python \
    python-dev\
    python-pip \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

#copy over and install the requirements
COPY ./misc/requirements.txt /var/www/app/app/requirements.txt
RUN pip install -r /var/www/app/app/requirements.txt

COPY ./misc/app_config.xml ./misc/app.conf /var/www/app/
RUN rm /etc/nginx/conf.d/default.conf && ln -s /var/www/app/app.conf /etc/nginx/conf.d/
COPY ./code /var/www/app/app/

WORKDIR /var/www/app

ENV MONGO_HOST 0.0.0.0
ENV MONGO_PORT 27017

EXPOSE 80

CMD ["/bin/bash", "-c", "nginx; uwsgi -x /var/www/app/app_config.xml > /dev/null 2>&1"]

