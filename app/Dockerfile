FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app

ENV PYTHONPATH=/app

EXPOSE 8501

CMD ["streamlit", "run", "app/app_streamlit_ui.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
