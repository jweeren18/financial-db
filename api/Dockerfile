FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy only needed packages
COPY api /app/api
COPY database /app/database
COPY data /app/data
COPY app /app/app

ENV PYTHONPATH=/app

EXPOSE 8001

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8001"]
