     # Define the name of the image that will be using
     FROM nikolaik/python-nodejs:python3.9-nodejs22-alpine

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


    # install nodejs usin unofficial builds
    # ENV NODE_PACKAGE_URL  https://unofficial-builds.nodejs.org/download/release/v22.2.0/node-v22.2.0-linux-x64-musl.tar.gz
    # RUN

    # RUN apk add libstdc++ &&\
    # wget $NODE_PACKAGE_URL &&\
    #   mkdir -p /app/nodejs &&\
    #   tar -zxvf *.tar.gz --directory /app/nodejs --strip-components=1 &&\
    #    rm *.tar.gz &&\
    #   ln -s /app/nodejs/bin/node /usr/local/bin/node &&\
    #   ln -s /app/nodejs/bin/npm /usr/local/bin/npm &&\

    # RUN mkdir -p static/css && cd static/css && npm init -y && \
    #       npm install tailwindcss postcss-cli autoprefixer &&\
    #       npm init -y && \
    #       npm i -D tailwindcss

    # RUN   npx tailwindcss init && \
    #       npx postcss styles.css -o compiled.css

    #  # Install curl, bash, and Node.js using NVM (gets stuck)
    #     RUN apk add --update build-base linux-headers curl bash && \
    #     curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && \
    #     /bin/bash -c "source ~/.nvm/nvm.sh && nvm install 18 &&  nvm use 18" \
    #     node -v && npm -v &&\
    #     # /bin/bash -c "source ~/.nvm/nvm.sh && nvm install 20.13.1 && nvm use 20.13.1"&& \
    #     # Create the static/css directory, initialize a new Node.js project, and install dependencies
    #     mkdir -p static/css && cd static/css && npm init -y && \
    #     npm install tailwindcss postcss-cli autoprefixer && \
    #     npx tailwindcss init && \
    #     npx postcss styles.css -o compiled.css

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
             django-user\
             && chown django-user:django-user -R /home

     # actualiza la variable de ambiente dentro de la imagen
     # el atributo path, para no evitar correr /py/bin cada vez que corremos un comando
     # aca le agregamos el system path
     ENV PATH="/py/bin:$PATH"

    RUN SECRET_KEY=nothing python src/django/manage.py tailwind install --no-input;
    RUN SECRET_KEY=nothing python src/django/manage.py tailwind build --no-input;
    RUN SECRET_KEY=nothing python src/django/manage.py collectstatic --no-input;

     # cambiamos el usuario que se utilizara en adelante (para evitar usar el root-user)
     # USER django-user

     CMD ["python", "manage.py", "runserver"]

