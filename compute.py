# Filename: compute.py : Contains functionalities of the web application for error handling and generating transcripts as PDFs.

# Import relevant libraries
import time
import re
import os
from datetime import datetime
import shutil
from datetime import date
import csv
from fpdf import FPDF  # fpdf class

# PDF class for creating the transcripts. PDF class inherits from the builtin FPDF class in python. 
class PDF(FPDF):

	# Lines function creates all the lines and puts the data inside the pdf
	def lines(self, pdf_h, pdf_w, file, name, Prog, course, roll_sem, ct_roll, cc_roll, spi_roll, cpi_roll, file_1=None, file_2=None):

		month_num= {1:"Jan",2:"Feb",3:"March",4:"April",5:"May",6:"June",7:"July",8:"Aug",9:"Sep",10:"Oct", 11:"Nov", 12:"Dec"}

		# Create borders of the pdf
		self.set_line_width(0.0)
		self.line(5,30,pdf_h-5,30)
		self.line(5.0,5.0, pdf_h-5 ,5.0) # top one
		self.line(5.0,pdf_w-5 , pdf_h-5 , pdf_w-5) # bottom one
		
		self.line(5.0,5.0,5.0, pdf_w-5) # left one
		self.line(pdf_h-5,5.0,pdf_h-5, pdf_w-5) # right one
		self.line(40, 5, 40, 30)
		self.line(pdf_h-40, 5, pdf_h-40, 30)

		# Put IITP logo and text "INTERIM TRANSCRIPT" below the logo on the left and right corners of pdf
		self.set_xy(10.0,8.0)
		self.image(name='IITP_logo.png', type='png', w=24, h=18)
		self.set_xy(14.0,25.0)
		self.set_font('Arial', 'BU', 8)
		self.cell(w=19.0, h=5.0, align='C', txt="INTERIM TRANSCRIPT", border=0)

		self.set_xy((pdf_h-40)+5,8.0)
		self.image(name='IITP_logo.png', type='png', w=24, h=18)
		self.set_xy((pdf_h-40)+9,25.0)
		self.set_font('Arial', 'BU', 8)
		self.cell(w=19.0, h=5.0, align='C', txt="INTERIM TRANSCRIPT", border=0)

		# Create the rectangle which contains name, roll no., year of admission, programmme and course
		k= 40+((pdf_h-80-210)/2)
		self.rect(k, 32.0, 210, 10.0)

        # Get current date to obtain the current year
		todays_date = date.today()
		cur_yr = int(str(todays_date.year)[-2:])

		if int(file[:2]) <= cur_yr:
			year = str(cur_yr-1) + str(file[:2]) 
		elif int(file[:2]) > cur_yr:
			year = str(cur_yr-2) + str(file[:2])

		self.set_font('Arial', 'B', 8)
		self.text(x=k+2, y=35, txt="Roll No.:")
		self.text(x=k+15, y=35, txt= file)
		self.text(x=k+75, y=35, txt= "Name:")
		self.text(x=k+85, y=35, txt= name)
		self.text(x=k+175, y=35, txt= "Year of Admission: ")

		self.text(x=k+202, y=35, txt= year)
		self.text(x= k+2, y=40, txt="Programme: ")
		self.text(x= k+20, y=40, txt= Prog)
		self.text(x=k+75, y=40, txt= "Course:")
		self.text(x=k+87, y=40, txt= course)

		# Create the table of all the subjects taken by the student in each semester 
		col_width = [10,63,6,6,6]
		var_x = (pdf_h-10-(sum(col_width)*3))/4

		sem_x = 5 + var_x
		sem_y = 49

		line_height = 3
		t_x = 5 + var_x
		t_y = 50
		
		offset_x= 5 + var_x
		rect_x = 5 + var_x

		s = {}
		for sem in roll_sem.keys():

			if int(sem) in [4,7]:

				mx_row = max([len(roll_sem[str(i)]) for i in range(1, int(sem))])
				k = (mx_row*3) + 4 + 3 + 3 + 3
				self.line(5,t_y+ k - 3, pdf_h-5, t_y+ k - 3)
				sem_y = sem_y + k + 1
				table_y = t_y + k +1

				t_y = t_y + k + 1
				t_x = 5 + var_x
				offset_x = 5 + var_x
				sem_x = 5 + var_x
				rect_x = 5 + var_x
			
			table_y = t_y

			self.set_font('Arial', 'BU', 8)
			self.text(x= sem_x, y=sem_y, txt="Semester"+sem)

			data =[]
			data.append(["Sub Code", "Subject Name", "L-T-P", "CRD", "GRD"])
			data.extend(roll_sem[sem])
			s[int(sem)] = len(roll_sem[sem])

			self.set_font('Times','',6.0) 
			self.ln(0.5)

			for row in data:

				self.y= t_y

				for j,datum in enumerate(row):
					self.x= t_x
					self.cell(col_width[j], line_height, str(datum), border=1, align='C')
					t_x= t_x+col_width[j]

				t_x = offset_x
				t_y = t_y+line_height
				self.ln(line_height)

			# t_st = t_y
			self.rect(rect_x,t_y+2,91,3)

			# Display credits taken, cleared, cpi, and spi of each semester within a rectangle in the pdf
			self.set_font('Arial', 'B', 7)
			self.text(x= rect_x+2, y= t_y+2+2.5, txt= "Credits Taken:   " + str(ct_roll[sem]))
			self.text(x= rect_x+27, y= t_y+2+2.5, txt= "Credits Cleared:   " + str(cc_roll[sem]))
			self.text(x= rect_x+56, y= t_y+2+2.5, txt= "SPI: " + str(spi_roll[sem]))
			self.text(x= rect_x+71, y= t_y+2+2.5, txt= "CPI: " + str(cpi_roll[sem]))

			sem_x+= 91 + var_x
			t_x+= 91 + var_x
			t_y= table_y
			offset_x+= 91 + var_x
			rect_x+= 91 + var_x

		if len(roll_sem)%3 == 0:
			l_n = 3
		else:
			l_n = int(len(roll_sem)%3)

		# Create space for uploading seal and signature of the assistant registrar in the pdf 
		roll_sem_list = [int(i) for i in roll_sem.keys()]
		n = len(roll_sem)-l_n + 1

		mx_row = max([len(roll_sem[str(i)]) for i in roll_sem_list[-l_n:]])
		
		# Create the lines, set up the fonts and add the text of "Assistant Registrar (Academic)"
		self.line(5,table_y+((1+mx_row)*3)+4+3, pdf_h-5, table_y+((1+mx_row)*3)+4+3)
		self.line(pdf_h-54,table_y+(mx_row*3)+4+3+40, pdf_h-10, table_y+(mx_row*3)+4+3+40)
		self.set_font('Arial', 'B', 8)

		self.text(x= pdf_h-54, y= table_y+(mx_row*3)+4+3+40+3, txt= "Assistant Registrar (Academic)")
		self.set_font('Arial', 'B', 8)
		self.text(x=10,y=table_y+(mx_row*3)+4+3+40, txt= "Date Generated: ")
		self.line(33, table_y+(mx_row*3)+4+3+40+1, 59, table_y+(mx_row*3)+4+3+40+1)

		# Put the seal and signature in the pdf if the user uploaded them
		if file_1:
			path_1 = os.path.join("sample_input", file_1)
			self.set_xy(((pdf_h-10)/2)-20, table_y+((1+mx_row)*3)+4+3+20)
			self.image(name= path_1, type= file_1.split(".")[-1])

		if file_2:
			path_2 = os.path.join("sample_input", file_2)
			self.set_xy(pdf_h-51, table_y+(mx_row*3)+4+3+40-15)
			self.image(name= path_2, type= file_2.split(".")[-1])

		# datetime object containing current date and time
		# Put the date and time in the pdf
		now = datetime.now()
		dt = now.strftime("%d %b %Y, %H:%M")
		self.text(x= 33, y= table_y+(mx_row*3)+4+3+40, txt= dt)

	# Put the header text of the pdf
	def heading_A4_A3(self,pdf_h, pdf_w):

		self.add_font('gargi', 'B', 'gargi.ttf', uni=True) 
		self.set_font('gargi', 'B', 22)
		# self.add_font('MANGAL', 'B', 'MANGAL.TTF', uni=True) 
		# self.set_font('MANGAL', 'B', 22)
		self.text(x=40+((pdf_h-80)/3)-15, y= 13, txt="भारतीय प्रौद्योगिकी संस्थान अंटार्कटिका")

		self.set_font('Times', 'B', 18)
		self.text(x=40+((pdf_h-80)/4)-35, y= 21, txt="I n d i a n     I n s t i t u t e     o f     T e c h n o l o g y     A n t a r c t i c a")
		self.set_font('Times', 'B', 15)
		self.text(x=40+((pdf_h-80)/2)-20, y = 29, txt="Transcript")
		# self.set_font('Arial', 'B', 15)
		# self.cell(w=50, h=1.0, align='C', txt="Transcript", border=0)

# Obtain the data from names-roll csv, grades csv and subjects_master csv for writing the data into the pdf
def obtain_data():

	# Open and read names-roll.csv file and create a dictionary roll_2_name which has name and roll no. mapping
	with open("sample_input//names-roll.csv", 'r') as csvfile:

		reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
		roll_2_name= {}

		for row in reader:
			roll_2_name[row[0]] = row[1]
		roll_2_name.pop("Roll")

	# Open and read grades.csv file and create a dictionary info_roll which has info of all the roll numbers
	with open("sample_input//grades.csv", 'r') as csvfile:

		reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
		info_roll={}

		for row in reader:

			if row[0]!="Roll":

				# Create a key with roll no. if roll no. is not present in the info_roll dictionary 
				if row[0] not in info_roll.keys():
					info_roll[row[0]]= {}
					
				# Create a key with semester if semester is not present in the dictionary value of roll no. key
				if row[1] not in info_roll[row[0]].keys():
					info_roll[row[0]][row[1]]=[row[2:]]
				else:
					info_roll[row[0]][row[1]].append(row[2:])

	# Grade map dictionary for mapping grades to their numeric equivalent
	grade_map={"aa":10,"aa*":10,"ab":9,"ab*":9,"bb":8," bb*": 8,"bc":7,"bc*":7,"cc":6,"cc*":6,"cd":5,"cd*":5,"dd":4,"dd*":4,"f*":0,"f":0,"i":0,"i*":0}

	# Open and read subjects_master.csv file and create a dictionary sub_info which has the subject info and subject names
	with open("sample_input//subjects_master.csv", 'r') as csvfile:

		reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
		sub_info={}

		for row in reader:
			if row[0]!="subno":
				sub_info[row[0]]= row[1:4]

	# Initialize SPI, Credit, Total_Credit, CPI dictionaries
	SPI= {}
	Credit_clear={}
	Credit_taken={}
	CPI={}

	# Assign data obtained from info_roll dictionary to the above initialized dictionaries
	for roll in info_roll.keys():

		SPI[roll]={}
		Credit_clear[roll]={}
		Credit_taken[roll]={}
		CPI[roll]={}

		cred=0
		cpi_num=0

		for sem in info_roll[roll].keys():

			num=0
			credit_clear=0
			credit_taken =0

			for item in info_roll[roll][sem]:

				# Convert grade obtained to lower case 
				ch1=""
				for ch in item[2]:

					# Check using ASCII value if the character is in lower case or upper case
					if (ord(ch)>=65 and ord(ch)<=90) or (ord(ch)>=97 and ord(ch)<=122):
						ch1+=ch.lower()
					else:
						ch1+=ch

				num+= int(item[1])*grade_map[ch1]

				# Add credits of a semester for a particular roll number 
				credit_clear+= int(item[1])
				credit_taken+= int(sub_info[item[0]][2])

			# Add credits upto the end of a particular semester
			cred+= credit_clear

			# Calculate SPI for a particular semester
			spi= num/credit_clear
			cpi_num+=spi*credit_clear

			# Calculate CPI for a particular semester
			cpi= cpi_num/cred

			# Update the dictionary with calculated values
			SPI[roll][sem]=round(spi,2)
			Credit_taken[roll][sem]=credit_taken
			Credit_clear[roll][sem]=credit_clear
			CPI[roll][sem]= round(cpi,2)

	final_info_data={}

	# Create final_info_data dictionary from info_roll dictionary to create formatted data to be written to file
	for roll in info_roll.keys():

		final_info_data[roll] = {}

		for sem in info_roll[roll].keys():

			final_info_data[roll][sem]=[]
			idx=1

			for item in info_roll[roll][sem]:

				sem_list = []
				sem_list.append(item[0])
				sem_list.append(sub_info[item[0]][0])
				sem_list.append(sub_info[item[0]][1])
				sem_list.append(int(item[1]))
				sem_list.append(item[2])
				idx+=1

				final_info_data[roll][sem].append(sem_list)

	# return the data to be used by transcripts_roll_range and transcripts_all_range functions
	return roll_2_name, final_info_data, SPI, Credit_taken, Credit_clear, CPI

# Function for generating the transcripts of the range of roll numbers entered by user
def transcripts_roll_range(roll_range,file_1, file_2):

	# Fetch the data obtained by obtain_data function 
	roll_2_name, final_info_data, SPI, Credit_taken, Credit_clear, CPI = obtain_data()

	# Interpret the roll number range
	roll_list = roll_range.split("-")

	# Use regex expression matching to check if the range of roll numbers entered by user is correct
	roll_range_exp = r"(([0-9]+[01,11,12,13]+[a-zA-Z]+[0-9]+)(?:-)([0-9]+[01,11,12,13]+[a-zA-Z]+[0-9]+))"
	
	if bool(re.match(roll_range_exp, roll_range)):

		if (roll_list[0][4:6].upper() != roll_list[1][4:6].upper()) or (int(roll_list[0][6:]) > int(roll_list[1][6:])):
			return r"Enter a valid range of roll numbers..."

	else:
		return r"Enter a valid range of roll numbers..."

	# Pop the list of roll numbers which don't exist and generate transcripts for those roll numbers that exist 
	start = roll_list[0][6:].lstrip("0")
	end = roll_list[1][6:].lstrip("0")

	s1 = int(start)
	s2 = int(end) + 1

	t_roll_gen = []
	roll_not_exist = []
	roll_ne_s = "These roll numbers don't exist: "

	for i in range(s1, s2):

		dep = roll_list[0][:6]
		dep1 = ""

		for ch in dep:

			# Check using ASCII value if the character is in lower case or upper case
			if (ord(ch)>=65 and ord(ch)<=90) or (ord(ch)>=97 and ord(ch)<=122):
				dep1+=ch.upper()
			else:
				dep1+=ch

		if len(str(i))<2:
			roll_num = dep1 + "0"*(2-len(str(i))) +str(i)
		else:
			roll_num = dep1 + str(i)

		if roll_num not in roll_2_name.keys():
			roll_not_exist.append(roll_num)
		else:
			t_roll_gen.append(roll_num)

	# Create output directory if not found
	if not os.path.isdir("transcriptsIITP"):
		os.mkdir("transcriptsIITP")

	# Create PDF for each roll no. in t_roll_gen list
	for roll in t_roll_gen:

		# Change the roll number to uppercase, eg. 1401cs10 ->> 1401CS10 
		file =""

		for x in roll:

			if not (ord(x) >=48 and ord(x)<=57):
				file+= x.upper()
			else:
				file+=x

		# Extract the branch from the roll no. eg. extract CS from 0401CS02 
		d = [x.upper() for x in roll if not (ord(x) >=48 and ord(x)<=57)]
		d = "".join(d)

		# Course assigned to roll number on the basis of the branch extracted from roll number.
		if d=="CS":
			course = "Computer Science and Engineering"
		elif d=="ME":
			course = "Mechanical Engineering"
		elif d=="EE":
			course = "Electrical Engineering"
		elif d=="CH":
			course = "Chemical and Biochemical Engineering"
		elif d=="MME":
			course = "Metallurgical and Materials Engineering"
		elif d=="CE":
			course = "Civil Engineering"

		# Create the transcript on A3 size sheet if the roll number belongs to a btech student
		if roll[2:4] == "01":

			pdf_w=297
			pdf_h=420

			Prog = "Bachelor of Technology"
			pdf = PDF(orientation='L', unit='mm', format='A3') # Pdf object

		# Create the transcript on A4 size sheet if the roll number belongs to a Mtech, Phd or MSC student
		else:

			pdf_w=210
			pdf_h=297

			if roll[2:4] == "11":
				Prog = "Master of Technology"

			elif roll[2:4] == "12":
				Prog = "Master of Science"

			elif roll[2:4] == "21":
				Prog = "Doctor of Philosophy"

			pdf = PDF(orientation='L', unit='mm', format='A4') # Pdf object

		# Add the page to the initialized pdf
		pdf.add_page()

		# Call the functions of PDF class to create the lines, enter the text and data etc
		pdf.heading_A4_A3(pdf_h, pdf_w)

		pdf.lines(pdf_h, pdf_w, file, roll_2_name[roll], Prog, course, 
			      final_info_data[roll], Credit_taken[roll], Credit_clear[roll], SPI[roll], CPI[roll], file_1, file_2)

		# File error handling
		try:

			# Save the pdf into the "transcriptsIITP" folder
			pdf.output(os.path.join("transcriptsIITP",file+".pdf"), "F")
		
		except:
			return r"Please close the PDF files."

	# Pop the list of roll numbers on the GUI that are not existing
	if roll_not_exist!= []:
		return roll_ne_s+ "\n\n" +str(roll_not_exist)

# Function for generating the transcripts of all the roll numbers.
def transcripts_all_range(file_1, file_2):

	# Fetch the data obtained by obtain_data function 
	roll_2_name, final_info_data, SPI, Credit_taken, Credit_clear, CPI = obtain_data()

	# Create output directory if not found
	if not os.path.isdir("transcriptsIITP"):
		os.mkdir("transcriptsIITP")

	# Create PDF for each roll no. in final_info_data dictionary
	for roll in final_info_data.keys():

		file =""

		# Change the roll number to uppercase, eg. 1401cs10 ->> 1401CS10 
		for x in roll:

			if not (ord(x) >=48 and ord(x)<=57):
				file+= x.upper()
			else:
				file+=x

		# Extract the branch from the roll no. eg. extract CS from 0401CS02 
		d = [x.upper() for x in roll if not (ord(x) >=48 and ord(x)<=57)]
		d = "".join(d)

		# Course assigned to roll number on the basis of the branch extracted from roll number.
		if d=="CS":
			course = "Computer Science and Engineering"
		elif d=="ME":
			course = "Mechanical Engineering"
		elif d=="EE":
			course = "Electrical Engineering"
		elif d=="CH":
			course = "Chemical and Biochemical Engineering"
		elif d=="MME":
			course = "Metallurgical and Materials Engineering"
		elif d=="CE":
			course = "Civil Engineering"

		# Create the transcript on A3 size sheet if the roll number belongs to a btech student
		if roll[2:4] == "01":

			pdf_w=297
			pdf_h=420

			Prog = "Bachelor of Technology"
			pdf = PDF(orientation='L', unit='mm', format='A3') # Pdf object

		# Create the transcript on A4 size sheet if the roll number belongs to a Mtech, Phd or MSC student
		else:

			pdf_w=210
			pdf_h=297

			if roll[2:4] == "11":
				Prog = "Master of Technology"

			elif roll[2:4] == "12":
				Prog = "Master of Science"

			elif roll[2:4] == "21":
				Prog = "Doctor of Philosophy"

			pdf = PDF(orientation='L', unit='mm', format='A4') # Pdf object

		# Add the page to the initialized pdf
		pdf.add_page()

		# Call the functions of PDF class to create the lines, enter the text and data etc
		pdf.heading_A4_A3(pdf_h, pdf_w)

		pdf.lines(pdf_h, pdf_w, file, roll_2_name[file], Prog, course, 
			      final_info_data[roll], Credit_taken[roll], Credit_clear[roll], SPI[roll], CPI[roll], file_1, file_2)

		# File error handling
		try:

			# Save the pdf into the "transcriptsIITP" folder
			pdf.output(os.path.join("transcriptsIITP",file+".pdf"), "F")
			
		except:
			return r"Please close the PDF files."