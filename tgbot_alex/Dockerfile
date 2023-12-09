FROM python:3.10
WORKDIR /agent5_00
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD python bot.py