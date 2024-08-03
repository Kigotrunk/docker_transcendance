FROM alpine:3.20

WORKDIR /app

COPY requirements.txt /app/
COPY manage.py /app/

RUN apk update && apk upgrade
RUN apk add --no-cache alpine-sdk build-base sdl2 libffi-dev openssl-dev bzip2-dev zlib-dev readline-dev sqlite-dev python3-dev py3-pip postgresql-dev python3 gcc musl-dev linux-headers jpeg-dev freetype-dev sdl2-dev sdl2_image sdl2_mixer sdl2_ttf tzdata

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]