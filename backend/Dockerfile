FROM python:3.11


ENV PYTHONUNBUFFERED=1


RUN apt-get update \
  && apt-get install -y tesseract-ocr tesseract-ocr-rus \
  && apt-get install -y wget gnupg unzip curl \
  && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update \
  && apt-get install -y google-chrome-stable

RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
  && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
  && rm /tmp/chromedriver.zip


WORKDIR /backend
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 8000
