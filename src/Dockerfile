FROM ubuntu:20.04

RUN apt update
RUN apt install nginx -y
RUN echo 'hello wordl' > /var/www/html/index.html

EXPOSE 80
CMD nginx -g 'daemon off;'