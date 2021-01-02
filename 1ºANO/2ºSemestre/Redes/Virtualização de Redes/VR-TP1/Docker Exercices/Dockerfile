FROM ubuntu

MAINTAINER GrupoX <pg41840@uminho.pt>

RUN apt-get update

RUN apt-get install -y nginx && apt-get clean

EXPOSE 80

ENTRYPOINT ["/usr/sbin/nginx"]

CMD ["start”, “-g"]
