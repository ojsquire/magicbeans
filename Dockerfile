FROM tiangolo/uvicorn-gunicorn:python3.8
RUN mkdir /magicbeans
COPY . /magicbeans
WORKDIR /magicbeans
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008"]
EXPOSE 8008