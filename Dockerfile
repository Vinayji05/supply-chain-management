# Dockerfile: builds C++ simulator and runs Streamlit
FROM python:3.11-slim
RUN apt-get update && apt-get install -y g++ build-essential && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN g++ -O2 -std=c++17 -o src/simulator/simulate src/simulator/main.cpp
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit","run","streamlit_app/app.py","--server.port","8501","--server.address","0.0.0.0"]
