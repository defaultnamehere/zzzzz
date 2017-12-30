FROM python:2.7

LABEL maintainer="https://github.com/pielco11"

RUN git clone https://github.com/pielco11/zzzzz && cd zzzzz && pip install -r requirements.txt

WORKDIR /zzzzz

CMD ["echo", "[x] Need elasticsearch IP as arg."]
ENTRYPOINT ["python", "/zzzzz/fetcherToES.py"]
