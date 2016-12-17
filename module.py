### -*- coding: utf-8 -*- ###

class Test():
	name = {'name':'Название','type':'char','value':'40'}
	number = {'name':'Число','type':'int','value':'10'}
	text = {'name':'Текст','type':'text'}
	img = {'name':'Изображение','type':'image'}
	test_list = {'name':'Выбор','type':'enum','value':'\'Првый\',\'Второй\''}
	date = {'name':'Дата','type':'date','required':'True'}
	test_chek = {'name':'Выбор','type':'set','value':'\'Первый\',\'Второй\',\'Еще\',\'И еще\''}
	chek = {'name':'Checkbox','type':'tinyint','value':'1'}

class News():
	name = {'name':'Название','type':'char','value':'100','required':'True'}
	date = {'name':'Дата','type':'date'}
	text = {'name':'Текст','type':'text'}
	chek = {'name':'На главную','type':'tinyint','value':'1'}

class Articles():
	name = {'name':'Название','type':'char','value':'100','required':'True'}
	text = {'name':'Текст','type':'text'}