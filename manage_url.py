### -*- coding: utf-8 -*- ###

from view import main, admin_main, admin_tab, admin_add, admin_add_db, admin_del, admin_edit, admin_edit_db, upload_img, contact, make, archiv_ot, archiv_in

def manage(url,get):


	list_url = url.split('/')
	list_url = list_url[1:]

	if len(list_url) == 1:
		if list_url[0] == 'admin':
			return (admin_main())
		
		elif list_url[0] == '':
			return (main())

		elif list_url[0] == 'contact':
			return (contact())

		elif list_url[0] == 'make':
			return (make())

		elif list_url[0] == 'upload_img':
			return (upload_img())

		elif list_url[0] == 'archiv_ot':
			return (archiv_ot())

		elif list_url[0] == 'archiv_in':
			return (archiv_in())

		else:
			return ("<!DOCTYPE html><html lang=\"ru\"><head><meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\" /></head>Страница не найдена</html>")
	

	elif len(list_url) == 2:
		if list_url[0] == 'admin':
			return (admin_tab(list_url[1]))

		if list_url[0] == 'archiv_ot':
			if list_url[1] == 'video':
				return (video_list_ot())

			if list_url[1] == 'arts':
				pass

			if list_url[1] == 'foto':
				pass

			if list_url[1] == 'names':
				pass

			if list_url[1] == 'books':
				pass

			if list_url[1] == 'th':
				pass

		if list_url[0] == 'archiv_in':
			if list_url[1] == 'video':
				pass

			if list_url[1] == 'arts':
				pass

			if list_url[1] == 'foto':
				pass

			if list_url[1] == 'names':
				pass

			if list_url[1] == 'books':
				pass

			if list_url[1] == 'th':
				pass

		else:
			return ("<!DOCTYPE html><html lang=\"ru\"><head><meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\" /></head>Страница не найдена</html>")

	elif len(list_url) == 3:
		if list_url[0] == 'admin':
			if list_url[2] == 'add':
				return (admin_add(list_url[1]))

			elif list_url[2] == 'add_db':
				return (admin_add_db(list_url[1], get))

			else:
				return ("<!DOCTYPE html><html lang=\"ru\"><head><meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\" /></head>Страница не найдена</html>")

		else:
			return ("<!DOCTYPE html><html lang=\"ru\"><head><meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\" /></head>Страница не найдена</html>")

	elif len(list_url) == 4:
		if list_url[0] == 'admin':
			if list_url[3] == 'del':
				return (admin_del(list_url[1],list_url[2]))

			elif list_url[3] == 'edit':
				return (admin_edit(list_url[1],list_url[2]))

			elif list_url[3] == 'edit_db':
				return (admin_edit_db(list_url[1],list_url[2],get))

			else:
				return ("<!DOCTYPE html><html lang=\"ru\"><head><meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\" /></head>Страница не найдена</html>")
	
		else:
			return ("<!DOCTYPE html><html lang=\"ru\"><head><meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\" /></head>Страница не найдена</html>")
	else:
		return ("<!DOCTYPE html><html lang=\"ru\"><head><meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\" /></head>Страница не найдена</html>")