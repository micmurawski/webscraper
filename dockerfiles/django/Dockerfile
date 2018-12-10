FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
RUN set -e;

WORKDIR /app/
COPY backend/requirements/app.txt requirements/app.txt
RUN apk update && \
     apk upgrade -U -a && \
     apk add postgresql-dev && \
     apk add libxml2-dev && \
     apk add libxslt-dev && \
     apk add python3-dev && \
     apk add --virtual=build-dependencies \
	            freetype-dev \
	            jpeg-dev \
	            libffi-dev \
	            libpng-dev \
	            libwebp-dev \
	            openjpeg-dev \
	            tiff-dev \
	            zlib-dev && \
     set -e; \
     apk add --no-cache --virtual .build-deps \
         gcc \
         libc-dev \
         linux-headers && \
     pip3.6 install --upgrade pip && \
     pip3.6 install -U setuptools && \
     pip3.6 install -r requirements/app.txt && \
     apk del .build-deps;
ADD ./backend /app/
CMD ["uwsgi", "--ini", "uwsgi.ini"]