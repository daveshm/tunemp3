# Use an official Python runtime as a parent image
FROM us-central1-docker.pkg.dev/inference-front-end/infer/infer:1.2.3

# # Install necessary packages
# RUN apt-get update && apt-get install -y  \
#     cmake protobuf-compiler libprotoc-dev libsndfile1 redis-server \
#     && rm -rf /var/lib/apt/lists/*

# RUN python3 -m pip install click flask requests google-cloud-storage celery

RUN python3 -m pip install google-cloud-run
# Install necessary packages
# RUN apt-get update && apt-get install -y  \
#     strace \
#     && rm -rf /var/lib/apt/lists/*

# RUN python3 -m pip install so-vits-svc-fork

# Set the working directory
WORKDIR /app

# # Copy the current directory contents into the container at /app
COPY python.py /app
COPY infer.sh /app
RUN chmod -R 765 /app

EXPOSE 5000

# Define default command to run when the container starts
CMD ["sh", "-c", "python3 python.py"]

