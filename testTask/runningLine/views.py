import cv2
import numpy as np
import os
from django.http import HttpResponse
from django.utils.timezone import localtime, now
from .models import Request

def hello(requeste):
	return HttpResponse("Напишите в адресной строке Ваш текст после /")

def textGenerator(requeste, text):
	text = str(text)
	if text == "favicon.ico":
		return HttpResponse(f"""
			<h2>testTask</h2>
			<p>Ваш текст: {text}</p>
			""")
	infoBd = Request(userText = text, dateText = localtime(now()))#создаю объект модели Request
	infoBd.save()#cохраняю в БД
	# задаём параметры для отображения текста и записи видео
	fps = 24#задаём количество кадров
	path_to_save = 'C:\django'#путь сохранения видеофаййла
	video_path = os.path.join(path_to_save, "video" + ".mp4")#соединяет путь с именем файла
	font_face = cv2.FONT_HERSHEY_TRIPLEX#задание типа шрифта
	font_scale = 8.0#размер шрифта
	thickness = 8#толщина шрифта
	fourcc = cv2.VideoWriter.fourcc('m', 'p', '4', 'v')#сохраняем файл с помощью видеокодека FourCC

	# определяем размеры и цвет фонового изображения (background image)
	(width, higth), _ = cv2.getTextSize(text, font_face, font_scale, thickness)#записываем размеры текста
	bg_w, bg_h = 2*higth + width, 3 * higth#записываем размер фона
	bg_img = np.zeros((bg_h, bg_w, 3), np.uint8)#создание матрицы изображения
	bg_img[:,:,1] = 200 # заполняем матрицу в зелёный цвет 
	bg_img[:,:,0] = 13 # заполняем матрицу в синий цвет
	text_color = (255, 255, 255)#задаем цвет текста

	# накладываем текст на фоновое изображение и приводим к нужному размеру
	org = (int(higth / 2), int( 2*higth))#задаем координаты левого нижнего угла текста на картинке
	img_w_text = cv2.putText(bg_img, text, org, font_face, font_scale, text_color, thickness)#рисуем строку текста на фоне 
	target_img = cv2.resize(img_w_text, (int(100 * bg_w / bg_h), 100))#изменяем размер картинки под наши нужды

	# создаём VideoWriter и записываем кадры
	num_frames = fps * 3#задаём количество кадров
	step = (int(100 * bg_w / bg_h) - 100) / num_frames#задаём сдвиг
	video = cv2.VideoWriter(video_path, fourcc, fps, (100, 100))#создаём объект VideoWriter для записи видео
	
	#создаём цикл для покадровой записи
	print('WRiting ', text)
	for i in range(num_frames):
		window_start = round(step * i)#задаём шаг
		frame = target_img[:,window_start:window_start + 100]
		video.write(frame)#записываем кадр
	video.release()#освобождаю объект
	print('End wRiting ', text)
	return HttpResponse(f"""
			<h2>testTask</h2>
			<p>Ваш текст: {text}</p>
			""")#вывожу на экран текст пользователя, завершаю функцию
