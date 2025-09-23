FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt install lilypond

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main_app.py"]
