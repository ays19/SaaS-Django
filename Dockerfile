# Set the python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install os dependencies for our mini vm
RUN apt-get update && apt-get install -y \
    # for postgres
    libpq-dev \
    # for Pillow
    libjpeg-dev \
    # for CairoSVG
    libcairo2 \
    # other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the mini vm's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /tmp/requirements.txt

# copy the project code into the container's working directory
COPY . /code

# Install the Python project requirements
RUN pip install -r /tmp/requirements.txt
RUN pip install gunicorn

ARG DJANGO_DEBUG=0
ENV DJANGO_DEBUG=${DJANGO_DEBUG}

# DJANGO_SECRET_KEY is sensitive, so it must never be baked into the image via
# ARG/ENV (that leaves it readable in `docker history`/image layers forever).
# The commands below only need Django's settings to import successfully - they
# don't do anything cryptographic with the key - so we pass a disposable,
# build-only value inline to these two RUN steps. It never becomes an image
# layer. The real secret is supplied at container start time via your host's
# runtime environment variables (e.g. Railway's service "Variables" tab), not
# through this Dockerfile.
#
# database isn't available during build
# run any other commands that do not need the database
# such as:
RUN DJANGO_SECRET_KEY="build-time-only-unused-in-production" \
    python manage.py vendor_pull
# --ignore=input.css: django-allauth-ui ships its raw Tailwind v4 source file
# (allauth_ui/input.css, containing `@import "tailwindcss";`) alongside the
# compiled allauth_ui/output.css that templates actually use. Whitenoise's
# manifest storage tries to post-process every .css file it collects and
# chokes on that `@import`, treating "tailwindcss" as a missing relative file
# reference. input.css is never linked from any template, so it's safe to
# skip collecting it entirely.
RUN DJANGO_SECRET_KEY="build-time-only-unused-in-production" \
    python manage.py collectstatic --noinput --ignore=input.css
#whitenoise -> s3

# set the Django default project name
ARG PROJ_NAME="Saas_Django"

# create a bash script to run the Django project
# this script will execute at runtime when
# the container starts and the database is available
RUN printf "#!/bin/bash\n" > ./paracord_runner.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./paracord_runner.sh && \
    printf "python manage.py migrate --no-input\n" >> ./paracord_runner.sh && \
    printf "gunicorn ${PROJ_NAME}.wsgi:application --bind \"[::]:\$RUN_PORT\"\n" >> ./paracord_runner.sh

# make the bash script executable
RUN chmod +x paracord_runner.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the Django project via the runtime script
# when the container starts
CMD ["./paracord_runner.sh"]