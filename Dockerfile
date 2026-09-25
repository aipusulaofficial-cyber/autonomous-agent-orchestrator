FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python","-c","from job_runner import JobRunner; print('job runner ready')"]
