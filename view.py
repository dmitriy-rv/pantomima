### -*- coding: utf-8 -*- ###
import MySQLdb
import sys

from urlparse import urlparse, parse_qsl

import os
from tem_base import Template

from cgi import escape

def database(sql):
	db = MySQLdb.connect(host="localhost", user="root", passwd="admin", db="pant", charset='utf8')
	cursor = db.cursor()
	cursor.execute(sql)
	db.commit()
	db.close()

def is_number(str):
	try:
		float(str)
		return True
	except ValueError:
		return False

template_dir = os.path.join(os.path.dirname(__file__), 'template')

template_admin = os.path.join(os.path.dirname(__file__), 'template/admin')

def read_html(engine):
    html_file_path = os.path.join(template_dir, "%s.html" % engine)
    html = open(html_file_path,'r').read()

    return html

def read_admin_html(engine):
    html_file_path = os.path.join(template_admin, "%s.html" % engine)

    html = open(html_file_path,'r').read()

    #with open(html_file_path) as html_file:
    #   html = html_file.read()

    return html

def main():

	db = MySQLdb.connect(host="localhost", user="root", passwd="admin", db="pant", charset='utf8')
	cursor = db.cursor()
	sql = """SELECT * FROM news where chek = 1 order by id DESC limit 3;"""
	cursor.execute(sql)
	qr = cursor.fetchall()

	list_row = []
	for row in qr:
		name = row[3].encode("utf-8")
		text = row[2].encode("utf-8")
		temp_dict = {'name':name,'id':row[0],'data':row[1],'text':text[:300]}
		list_row.append(temp_dict)

	sql = """SELECT text  FROM articles where name = 'Главная';"""
	cursor.execute(sql)
	qr_text = cursor.fetchone()
	text = qr_text[0].encode("utf-8")


	db.commit()
	db.close()

	return Template(read_html('index')).render(tab = list_row, text = text)

def admin_main():

	file = open('app/base.txt', 'r')

	tab_name = []

	for line in file:
		temp_1 = line.split(';')
		tab_name.append(temp_1[0])

	file.close()

	return Template(read_admin_html('index')).render(tab = tab_name)

def admin_tab(table):

	db = MySQLdb.connect(host="localhost", user="root", passwd="admin", db="pant", charset='utf8')
	cursor = db.cursor()
	sql = """SELECT id,name FROM %(tab)s;"""%{"tab":table}
	cursor.execute(sql)
	qr = cursor.fetchall()

	list_row = []
	for row in qr:
		temp_name = row[1].encode("utf-8")
		temp_dict = {'name':temp_name,'id':row[0]}
		list_row.append(temp_dict)

	db.commit()
	db.close()

	return Template(read_admin_html('table')).render(list_name = list_row, tab_name = table)

def admin_add(table):

	file = open('../pant/app/base.txt', 'r')

	tab_list = []

	for line in file:
		temp_dict = dict()
		temp_1 = line.split(';')
		if temp_1[0] == table:
			for temp__1 in temp_1[1:-1]:
				temp_2 = temp__1.split('|')
				str_name = temp_2[0]
				str_prop = dict()
				for temp__2 in temp_2[1:-1]:
					temp_3 = temp__2.split(':')
					str_prop[temp_3[0]]=temp_3[1]
				temp_dict[str_name]=str_prop
			tab_list.append(temp_dict)
	file.close()

	tab_html = ''

	for item in tab_list:
		for temp in item:

			req = ''
			try:
				if item[temp]['required']:
					req = 'required'
			except:
				pass

			if item[temp]['type'] == "char":
				tab_html = tab_html + """ 
							<tr>
	                            <td>
	                                <label>
	                                    %(tlabel)s</label>
	                            </td>
	                            <td>
	                                <input type="text" class="medium" %(req)s name = "%(tname)s" />
	                            </td>
	                        </tr>"""%{"tlabel":item[temp]['name'], "tname":temp, "req":req}
			
			elif item[temp]['type'] == "int":
				tab_html = tab_html + """ 
							<tr>
	                            <td>
	                                <label>
	                                    %(tlabel)s</label>
	                            </td>
	                            <td>
	                                <input type="text" class="medium" %(req)s name = "%(tname)s" pattern="^[ 0-9]+$" />
	                            </td>
	                        </tr>"""%{"tlabel":item[temp]['name'], "tname":temp, "req":req}
			
			elif item[temp]['type'] == "enum" or item[temp]['type'] == "set":
				mp = 'size="1"'

				if item[temp]['type'] == "set":
					mp = 'multiple'

				temp_option = ''
				for temp_value in item[temp]['value'].split(','):
					temp_option = temp_option + """<option value = "%(value)s">%(value)s</option> """%{'value':temp_value[1:-1]}
				
				tab_html = tab_html + """  
								<tr>
		                            <td>
		                                <label>
		                                    %(tlabel)s</label>
		                            </td>
		                            <td>
		                            	<select required name="%(tname)s"  %(mp)s %(req)s>
		                                	%(str_value)s
		                                </select>
		                            </td>
		                        </tr>"""%{"tlabel":item[temp]['name'], "tname":temp, 'str_value':temp_option, "req":req, "mp":mp}

			elif item[temp]['type'] == "text":
				tab_html = tab_html + """ 
							<tr>
	                            <td>
	                                <label>
	                                    %(tlabel)s</label>
	                            </td>
	                            <td>
	                                <textarea id="editor1" rows="10" cols="80" %(req)s name = "%(tname)s" />
	                                </textarea>
	                                <script>
                						// Replace the <textarea id="editor1"> with a CKEditor
                						// instance, using default configuration.
                						CKEDITOR.replace( 'editor1' );
            						</script>
	                            </td>
	                        </tr>"""%{"tlabel":item[temp]['name'], "tname":temp, "req":req}
			
			elif item[temp]['type'] == "image":
				tab_html = tab_html + """ 
							<tr>
	                            <td>
	                                <label>
	                                    %(tlabel)s</label>
	                            </td>
	                            <td>
	                                <input type="file" name="%(tname)s" %(req)s  multiple accept="image/*" />
	                                <a href="" class="submit button" onclick="toggleInformer_1()">Загрузить файлы</a>
                					<div class="ajax-respond"></div>
	                            </td>
	                        </tr>"""%{"tlabel":item[temp]['name'],"tname":temp, "req":req}
			
			elif item[temp]['type'] == "date":
				tab_html = tab_html + """ 
							<tr>
	                            <td>
	                                <label>
	                                    %(tlabel)s</label>
	                            </td>
	                            <td>
	                                <input type="date" %(req)s name = "%(tname)s" />
	                            </td>
	                        </tr>"""%{"tlabel":item[temp]['name'], "tname":temp, "req":req}

			elif item[temp]['type'] == "tinyint":
				tab_html = tab_html + """ 
							<tr>
	                            <td>
	                                <label>
	                                    %(tlabel)s</label>
	                            </td>
	                            <td>
	                            <label>
	                            	<input type="radio" checked="checked" name="%(tname)s" value="0"/>
	                            	 Выкл
	                            </label> 
	                            <label>
	                            	<input type="radio" name="%(tname)s" value="1"/>
	                            	 Вкл
	                           	</label>
	                            </td>
	                        </tr>"""%{"tlabel":item[temp]['name'], "tname":temp}
			

	return Template(read_admin_html('add')).render(tab_name = table, tab = tab_html, html_addres = 'add_db')	

def admin_add_db(table, get):

	
	get_list = parse_qsl(urlparse('?'+get)[4])
	
	sql_title = ''
	sql_value = ''

	for item in get_list:
		sql_title =sql_title + item[0] +', '
		sql_value =sql_value + '\'' + item[1] + '\'' +', '

	sql = """insert into %(tname)s (%(title)s) values (%(value)s);"""%{'tname':table,'title':sql_title[:-2],'value':sql_value[:-2]}
	database(sql)
	
	return """<html><head><meta http-equiv=refresh content=\"1; url=http://127.0.0.1:8080/admin/%(tab)s\"></head></html>"""%{"tab":table}

def admin_del(table, id_name):

	sql = """delete from %(tname)s where id=%(id)s;"""%{'tname':table,'id':id_name}
	database(sql)

	return """<html><head><meta http-equiv=refresh content=\"1; url=http://127.0.0.1:8080/admin/%(tab)s\"></head></html>"""%{"tab":table}

def admin_edit(table, id_name):

	file = open('../pant/app/base.txt', 'r')

	tab_list = []

	for line in file:
		temp_dict = dict()
		temp_1 = line.split(';')
		if temp_1[0] == table:
			for temp__1 in temp_1[1:-1]:
				temp_2 = temp__1.split('|')
				str_name = temp_2[0]
				str_prop = dict()
				for temp__2 in temp_2[1:-1]:
					temp_3 = temp__2.split(':')
					str_prop[temp_3[0]]=temp_3[1]
				temp_dict[str_name]=str_prop
			tab_list.append(temp_dict)
	file.close()

	str_name =[]

	for item in tab_list:
		for temp in item:
			str_name.append(temp)


	str_line = ', '.join(str_name)




	db = MySQLdb.connect(host="localhost", user="root", passwd="admin", db="pant", charset='utf8')
	cursor = db.cursor()
	sql = """SELECT %(sname)s FROM %(tname)s where id=%(id)s;"""%{'sname':str_line,'tname':table, 'id':id_name}
	cursor.execute(sql)
	qr = cursor.fetchone()

	list_row = dict()

	for index,row in enumerate(qr):
		if is_number(row) == False:
			list_row[str_name[index]] = row.encode("utf-8")
		else:
			list_row[str_name[index]] = row	

	db.commit()
	db.close()



	tab_html = ''

	for item in tab_list:
		for temp in item:
			if item[temp]['type'] == "char" or "int":
				tab_html = tab_html + """  
							<tr>
	                            <td>
	                                <label>
	                                    %(tlabel)s</label>
	                            </td>
	                            <td>
	                                <input type="text" class="medium" name = "%(tname)s" value = "%(tvalue)s"/>
	                            </td>
	                        </tr>"""%{"tlabel":item[temp]['name'], "tname":temp, "tvalue":list_row[temp]}

			if item[temp]['type'] == "enum":
				temp_option = ''
				for temp_value in item[temp]['value'].split(','):
					temp_option = temp_option + """<option value = "%(value)s">%(value)s</option> """%{'value':temp_value[1:-1]}
				
				tab_html = tab_html + """  
								<tr>
		                            <td>
		                                <label>
		                                    %(tlabel)s</label>
		                            </td>
		                            <td>
		                            	<select multiple name="%(tname)s">
		                                	%(str_value)s
		                                </select>
		                            </td>
		                        </tr>"""%{"tlabel":item[temp]['name'], "tname":temp, 'str_value':temp_option}

	return Template(read_admin_html('add')).render(tab_name = table, tab = tab_html, html_addres = id_name+'/edit_db')

def admin_edit_db(table,id_str,get):
	
	get_list = parse_qsl(urlparse('?'+get)[4])
	
	sql_list = ''

	for item in get_list:
		sql_list =sql_list + item[0] +' = ' + '\'' + item[1] + '\'' +', '

	sql = """update %(tname)s set %(list)s where id=%(id)s;"""%{'tname':table,'list':sql_list[:-2],'id':id_str}
	database(sql)

	return """<html><head><meta http-equiv=refresh content=\"1; url=http://127.0.0.1:8080/admin/%(tab)s\"></head></html>"""%{"tab":table}

def upload_img(self, myFile):
	       # out = """<html>
       # <body>
       #     myFile length: %s<br />
       #     myFile filename: %s<br />
       #     myFile mime-type: %s<br />
       #     data: %s
       # </body>
       # </html>"""
        
        # Although this just counts the file length, it demonstrates
        # how to read large files in chunks instead of all at once.
        # CherryPy reads the uploaded file into a temporary file;
        # myFile.file.read reads from that.
	size = 0
	print 'get_all'

	file = open(myFile.filename, 'wb')
	file.write(myFile.file.read())
	file.close()

upload_img.exposed = True


def make():

	db = MySQLdb.connect(host="localhost", user="root", passwd="admin", db="pant", charset='utf8')
	cursor = db.cursor()

	sql = """SELECT text  FROM articles where name = 'Создатели';"""
	cursor.execute(sql)
	qr_text = cursor.fetchone()
	text = qr_text[0].encode("utf-8")


	db.commit()
	db.close()

	return Template(read_html('make')).render(text = text)

def contact():

	db = MySQLdb.connect(host="localhost", user="root", passwd="admin", db="pant", charset='utf8')
	cursor = db.cursor()

	sql = """SELECT text  FROM articles where name = 'Контакты';"""
	cursor.execute(sql)
	qr_text = cursor.fetchone()
	text = qr_text[0].encode("utf-8")


	db.commit()
	db.close()

	return Template(read_html('contact')).render(text = text)

def archiv_ot():

	return Template(read_html('archiv')).render(title = 'Отечественная пантомима', 
		video = 'archiv_ot/video', 
		arts = 'archiv_ot/arts',
		foto = 'archiv_ot/foto',
		names = 'archiv_ot/names',
		books = 'archiv_ot/books',
		th = 'archiv_ot/th')


def archiv_in():

	return Template(read_html('archiv')).render(title = 'Иностранная пантомима', 
		video = 'archiv_in/video', 
		arts = 'archiv_in/arts',
		foto = 'archiv_in/foto',
		names = 'archiv_in/names',
		books = 'archiv_in/books',
		th = 'archiv_in/th')