FROM python:3.10-slim

WORKDIR /app

COPY app.py backend.py ./

RUN pip install --no-cache-dir streamlit pandas

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
