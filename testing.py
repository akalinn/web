

def tester():

	count = 0
	try:
		correct = True;
		while 1:


			f = open("article\Article_"+str(count), 'r',encoding='utf-8')
			has_lines = 0
			for lines in f:
				if has_lines == 0 and int(lines) != count:
					print("\n\line # is not match ... on ",str(count))
					return -1;
				else:
					has_lines += 1


				print(lines,end='')
				if has_lines != 0 and len(lines) > 10:
					has_lines += 1

			if has_lines < 8:
				print("\n\nHas empty lines ... on ",str(count))
				return -1;

			count += 1


		print("\n\nAll files are correct")
		return 0;



	except FileNotFoundError:
		print("\n\nHas ",str(count)," files")
		return -1;


if __name__ == "__main__":
    tester()