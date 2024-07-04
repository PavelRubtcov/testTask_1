from django.db import models
#создание модели для записи в БД
class Request(models.Model):
	userText = models.TextField()#текст пользователя неограниченной длины
	dateText = models.DateTimeField()#дата и время записи
# Create your models here.
