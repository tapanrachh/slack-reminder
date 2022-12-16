FROM python:3.8
ENV TZ="Asia/Kolkata"



COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pwd

RUN ls

# copy directory
RUN mkdir /app


RUN chown -R 1000 /app

RUN ls -l

Run date

# set work directory
WORKDIR /app

RUN pwd

RUN ls

COPY . .


RUN ls

EXPOSE 1337

USER 1000

CMD [ "python", "./server.py" ]
