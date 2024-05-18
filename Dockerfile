# Define the name of the image that will be using
FROM python:3.9-alpine3.13
LABEL maintainer="quien_mantiene_esto"

# Esto para mostrar los outputs de python en la consola inmediatamente
ENV PYTHONUNBUFFERED 1

# Copia el archivo requirements de nuestra maquina la carpeta /tmp de la imagen contenedor
COPY ./requirements.txt /tmp/requirements.txt

# Add dev requirements to container tmp file
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copia la carpeta app (que crearemos usando Django)
COPY . /app

# Seteamos el directorio defauilt donde se correran  los comandos
WORKDIR  /app

# Exponemos el puerto
EXPOSE 8000

# define build argument called DEV and set it to false
#( this will be overriden by docker-compose file's value of DEV arg)
ARG DEV=false

# RUN -> Comando para instalar las dependencias
# Utliza todo concatenado para evitar crear muchas capas de imagenes
# si se utilizara un RUN por cada comando
#1 crea virtual env
RUN python -m venv /py && \
    # instala pip en el venv
    /py/bin/pip install --upgrade pip && \
    # add postgresdb adaptor
    apk add --update --no-cache postgresql-client &&\
    apk add --update --no-cache --virtual .tmp-build-deps\
        build-base postgresql-dev musl-dev &&\
    # instala requirements
    /py/bin/pip install -r /tmp/requirements.txt &&\
    # Add logic in case dev mode is true to install dev dependencies
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
        # fi is shell sintax to end if block
    fi && \
    # remueve el directorio tmp para que quede liviana y prolijo nomas
    rm -rf /tmp &&\
    # remueve las dependencias que se instalaron para instalar postgres
    apk del .tmp-build-deps &&\
    # agrega un nuevo usuario en la imagen para evitar usar el root user
    # de la imagen alpine del contenedor
    adduser \
        --disabled-password \
        --no-create-home \
        #especifica el nombre del usuario
        django-user

RUN chown -R django-user ./src
    
# actualiza la variable de ambiente dentro de la imagen
# el atributo path, para no evitar correr /py/bin cada vez que corremos un comando
# aca le agregamos el system path
ENV PATH="/py/bin:$PATH"

# cambiamos el usuario que se utilizara en adelante (para evitar usar el root-user)
USER django-user