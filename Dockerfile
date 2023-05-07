FROM python:3.9
ENV PYTHONUNBUFFERED 1

WORKDIR /shop

COPY requirements.txt /shop
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install django-debug-toolbar && pip install django-simple-captcha && pip install djangorestframework

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]