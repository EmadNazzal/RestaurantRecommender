# FROM python:3.11-slim-buster

# WORKDIR /apps/backend

# COPY ./apps/backend .

# RUN python3 -m venv /opt/venv && \
#     /opt/venv/bin/pip install --upgrade pip && \
#     /opt/venv/bin/pip install -r requirements.txt && \
#     chmod +x /apps/backend/entrypoint.sh

# CMD [ "/apps/backend/entrypoint.sh" ]


FROM python:3.11-slim

# Set working directory
WORKDIR /apps/backend

# Install psql and other dependencies
RUN apt-get update && apt-get install -y postgresql-client redis-server procps nano

# Copy the requirements file into the container
COPY ./apps/backend/requirements.txt /apps/backend/

# Install dependencies
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r /apps/backend/requirements.txt

# Copy the rest of the application code
COPY ./apps/backend /apps/backend

# Ensure the entrypoint script is executable
RUN chmod +x /apps/backend/entrypoint.sh

# Set the environment path
ENV PATH="/opt/venv/bin:$PATH"

# Start the entrypoint script
CMD ["/apps/backend/entrypoint.sh"]
