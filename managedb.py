### -*- coding: utf-8 -*- ###
import MySQLdb
import sys
import os


import module


old_list = []
old_tab = []


# Вынимаем из файла информацию, и преобразуем ее в список словарей

file = open('base.txt', 'r')

for line in file:
	temp_dict = dict()
	temp_1 = line.split(';')
	temp_dict['title'] = temp_1[0]
	old_tab.append(temp_1[0])
	for temp__1 in temp_1[1:-1]: 
		temp_2 = temp__1.split('|')
		str_name = temp_2[0]
		str_prop = dict()
		for temp__2 in temp_2[1:-1]:
			temp_3 = temp__2.split(':')
			str_prop[temp_3[0]]=temp_3[1]
		temp_dict[str_name]=str_prop
	old_list.append(temp_dict)

file.close()

# Обрабатываем входящую информацию



new_list = []
new_tab = []
# Преобразуем информацию из объектов в строку со словарями

for i in dir(module):  #Извлекаем все таблицы по очереди
	temp_dict = dict() 
	attr = getattr(module, i)
	try:
		issubclass(attr, object)
		new_tab_name = attr.__name__
		temp_dict['title'] = new_tab_name
		new_tab.append(new_tab_name)
		for item in attr.__dict__:
			if item != "__module__":
					if item != "__doc__":
						temp_dict[item] = attr.__dict__[item]
		new_list.append(temp_dict)		
	except:
		pass

temp_new = set(new_tab)
temp_old = set(old_tab)

equal_tab = temp_new & temp_old
diff_tab_add = temp_new - temp_old
diff_tab_del = temp_old - temp_new

sql = ''


for item in diff_tab_add:

	sql_attr = ''

	for temp_dict in new_list:
		if item == temp_dict['title']:
			for temp_attr in temp_dict:
				if temp_attr != 'title':
					if temp_dict[temp_attr]['type'] == 'text':
						sql_attr = sql_attr + temp_attr + ' ' + temp_dict[temp_attr]['type']+','
					elif temp_dict[temp_attr]['type'] == 'image':
						sql_attr = sql_attr + temp_attr + ' ' + 'char(100),'
					elif temp_dict[temp_attr]['type'] == 'date':
						sql_attr = sql_attr + temp_attr + ' ' + 'date,'
					else:
						sql_attr = sql_attr + temp_attr + ' ' + temp_dict[temp_attr]['type'] + '(' + temp_dict[temp_attr]['value'] + ')'+','
	sql = sql + 'create table '+item+' (ID int NOT NULL AUTO_INCREMENT, PRIMARY KEY (ID),'+ sql_attr[:-1]+');'			

for item in diff_tab_del:
	sql = sql + ' drop table '+item+';'



for item in equal_tab:
	
	new_str_name = []
	old_str_name = []
	new_str_dict = dict()
	old_str_dict = dict()
	

	for temp_title in new_list:
		if item == temp_title['title']:
			new_str_dict = temp_title
			
	
	for temp_title in old_list:
		if item == temp_title['title']:
			old_str_dict = temp_title
	
	for temp_str in new_str_dict:
		if temp_str != 'title':
			new_str_name.append(temp_str)

	for temp_str in old_str_dict:
		if temp_str != 'title':
			old_str_name.append(temp_str)

	temp_new_str = set(new_str_name)
	temp_old_str = set(old_str_name)


	equal_str = temp_new_str & temp_old_str
	diff_str_add = temp_new_str - temp_old_str
	diff_str_del = temp_old_str - temp_new_str

	for temp in diff_str_add:
		if new_str_dict[temp]['type'] == 'text':
			sql = sql + ' alter table ' + item + ' add ' + temp + ' ' + new_str_dict[temp]['type'] + ';'
		elif new_str_dict[temp]['type'] == 'image':
			sql = sql  + ' alter table ' + item + ' add ' + temp + ' ' + 'char(100);'
		elif new_str_dict[temp]['type'] == 'date':
			sql = sql  + ' alter table ' + item + ' add ' + temp + ' ' + 'date;'
		else:
			sql = sql + ' alter table ' + item + ' add ' + temp + ' ' + new_str_dict[temp]['type'] + ' (' + new_str_dict[temp]['value'] + ');'

	for temp in diff_str_del:
		sql = sql + ' alter table ' + item + ' drop column ' + temp +';'

	for temp in equal_str:
		if new_str_dict[temp] != old_str_dict[temp]:
			if new_str_dict[temp]['type'] == 'text':
				sql = sql + ' alter table ' + item + ' change ' + temp + ' ' + temp + ' ' +  new_str_dict[temp]['type'] + ';'
			elif new_str_dict[temp]['type'] == 'image':
				sql = sql  + ' alter table ' + item + ' change ' + temp + ' ' + 'char(100);'
			elif new_str_dict[temp]['type'] == 'date':
				sql = sql  + ' alter table ' + item + ' add ' + temp + ' ' + 'date;'
			else:
				sql = sql + ' alter table ' + item + ' change ' + temp + ' ' + temp + ' ' +  new_str_dict[temp]['type'] + ' (' + new_str_dict[temp]['value'] + ');'


print sql

if sql != '':

	db = MySQLdb.connect(host="localhost", user="root", passwd="admin", db="pant", charset='utf8')
	cursor = db.cursor()
	#sql = """CREATE TABLE %(tname)s (%(lname)s %(set)s);"""%{"tname":'jorn', "lname":'number', "set":'int'}
	cursor.execute(sql)
	#db.commit ()
	db.close()

	print "base has been changed"
else:
	print "No changes"


file = open('base.txt', 'w')

for i in dir(module):
	lst = []
	if i != 'model':
		attr = getattr(module, i)
		try:
			issubclass(attr, object)
			name = attr.__name__
			lst.append(name) #Заголовок таблицы
			lst.append(';')

			listKeys = attr.__dict__.keys()
			for i in listKeys:
				if i != "__module__":
					if i != "__doc__":
						lst.append(i) #Название строки
						lst.append('|')

						dic_pr = attr.__dict__.get(i)
						for key in dic_pr:
							lst.append(key) #ключ
							lst.append(':')
							lst.append(dic_pr[key]) #значение
							lst.append('|')				
						lst.append(';')
			file.write("".join(lst) + '\n')
		except:
			pass
		
file.close()

print "File rewrited"