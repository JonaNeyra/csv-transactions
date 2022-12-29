FROM public.ecr.aws/lambda/python:3.8
LABEL maintainer="Jonathan Jorge Neyra Nieves <neyranievesjonathan@gmail.com>"

# Librerias necesarias para las dependencias
RUN yum install -y sudo \
        curl \
        git \
        libc-dev \
        libpq-dev \
        postgresql-devel \
        python3-dev \
        gcc \
        build-base

# Espacio de trabajo y clonacion del proyecto
ENV WORKDIR "${LAMBDA_TASK_ROOT}"
WORKDIR $WORKDIR
COPY . "${LAMBDA_TASK_ROOT}"

# Instalables por defecto Amazon
RUN pip install --upgrade pip && pip install wheel awscli

# RIE
RUN pip install awslambdaric --target "${LAMBDA_TASK_ROOT}"

# Dependencias Locales
RUN pip install -r requirements-dev.txt --target "${LAMBDA_TASK_ROOT}"

# Libreria para ejecutar la Emulacion
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie

# Permisos para el punto de acceso
RUN chmod 755 /usr/bin/aws-lambda-rie .docker/ric-entrypoint.sh

# Punto de Accceso
ENTRYPOINT [ ".docker/ric-entrypoint.sh" ]

CMD [ "src/handler.handle" ]