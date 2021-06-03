FROM python:3

ADD requirements.txt .
ADD main.py .

#Pip command without proxy setting
RUN pip install -r requirements.txt

CMD ["python","-i","main.py"]
