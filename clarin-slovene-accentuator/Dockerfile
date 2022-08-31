FROM tensorflow/tensorflow:2.6.0-gpu

# Create base directory
RUN mkdir app
WORKDIR app

# Copy required files
ADD requirements.txt ./
ADD src ./src

# Create empty data folder. Required data must be mounted at runetime.
RUN mkdir data

# Install dependencies
RUN pip install -U pip
RUN pip install -r requirements.txt

# Run service
WORKDIR src
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8080"]
