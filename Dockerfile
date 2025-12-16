FROM python:3.13.9

RUN pip install awscli

COPY entrypoint.sh entrypoint.sh

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

ADD requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update

RUN apt-get install poppler-utils -y

COPY conf/** /conf/

COPY controllers/** /controllers/

COPY models/** /models/

COPY routers/** /routers/

COPY services/** /services/

COPY swagger/** /swagger/

COPY utils/** /utils/

ADD api.py .