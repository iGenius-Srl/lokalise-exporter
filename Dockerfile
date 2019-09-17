FROM python:3.7

RUN pip install --upgrade igenius-lokalise-exporter

CMD ["lokalise-exporter"]