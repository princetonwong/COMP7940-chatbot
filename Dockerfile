FROM python:latest
COPY chatbot.py .
COPY Database.py .
COPY School.py .
COPY Utilities.py .
COPY Paper.py .
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT python chatbot.py