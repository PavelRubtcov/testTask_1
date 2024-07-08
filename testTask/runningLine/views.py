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
	ws_h = 400#высота видео в пикселях
	ws_w = 400#ширина видео в пикселях
	wh = ws_w/ws_h
	fps = 24.0#задаём количество кадров
	path_to_save = '/content/testTask_1'#путь сохранения видеофаййла
	video_path = os.path.join(path_to_save, "video" + ".mp4")#соединяет путь с именем файла
	font_face = cv2.FONT_HERSHEY_TRIPLEX#задание типа шрифта
	font_scale = 8.0#размер шрифта
	thickness = 8#толщина шрифта
	fourcc = cv2.VideoWriter_fourcc(*'MP4V')#сохраняем файл с помощью видеокодека FourCC

	# определяем размеры и цвет фонового изображения (background image)
	(width, higth), _ = cv2.getTextSize(text, font_face, font_scale, thickness)#записываем размеры текста
	bg_w, bg_h = int((6*higth*wh)) + width, 3 * higth#записываем размер фона
	bg_img = np.zeros((bg_h, bg_w, 3), np.uint8)#создание матрицы изображения
	bg_img[0:bg_h//2,:,1] = 200 # заполняем матрицу в зелёный цвет [y , x]
	bg_img[:,0:bg_w//2,0] = 53 # заполняем матрицу в синий цвет
	text_color = (255, 255, 255)#задаем цвет текста

	# накладываем текст на фоновое изображение и приводим к нужному размеру

	koef = ws_w / bg_w#коэффициент перевода 
	org = (int((3*higth*wh)), int(2 * higth))#int(higth / 2)#задаем координаты левого нижнего угла текста на картинке
	img_w_text = cv2.putText(bg_img, text, org, font_face, font_scale, text_color, thickness)#рисуем строку текста на фоне 
	target_img = cv2.resize(img_w_text, (int(((bg_w/bg_h)*ws_h) + 2*ws_w) , ws_h)) #(int(((bg_w/bg_h)*ws_h)), ws_h))#изменяем размер картинки под наши нужды

	# создаём VideoWriter и записываем кадры
	time = 3#длительность видео в секундах
	num_frames = int(fps * time)#задаём количество кадров
	#step = int((round(width*ws_h/bg_h) + ws_w)/num_frames)#(int(100 * bg_w / bg_h) - 100) / num_frames#задаём сдвиг
	#step = int(((((bg_w/bg_h)*ws_h) - ws_w)/num_frames))
	video = cv2.VideoWriter(video_path, fourcc, fps, (ws_w, ws_h))#создаём объект VideoWriter для записи видео
	step = int((3*higth*wh + width)/num_frames)
	#создаём цикл для покадровой записи
	print('WRiting ', text)
	print(width, higth, bg_w, bg_h, step,num_frames, int(((bg_w/bg_h)*ws_h)), len(target_img))
	step = int((bg_w-3*higth)/num_frames)
	for i in range(num_frames):
		bg_img = np.zeros((bg_h, bg_w, 3), np.uint8)
		bg_img[0:,:,1] = 200 # заполняем матрицу в зелёный цвет [y , x]
		bg_img[:,:,0] = 100 # заполняем матрицу в синий цвет
		img_w_text = cv2.putText(bg_img, text, org, font_face, font_scale, text_color, thickness)#рисуем строку текста на фоне 
		target_img = cv2.resize(img_w_text, (int(((bg_w/bg_h)*ws_h) + 2*ws_w) , ws_h)) #(int(((bg_w/bg_h)*ws_h)), ws_h))
		frame = target_img[:,0:ws_w]
		video.write(frame)#записываем кадр
		org = (int((2.5*higth*wh)) - i*step, int(2 * higth))
		print(org, i)
	video.release()#освобождаю объект
	
	return HttpResponse(f"""
			<h2>testTask</h2>
			<p>Ваш текст: {text}</p>
			""")#вывожу на экран текст пользователя, завершаю функцию
