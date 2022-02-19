# Filename: app.py : Execute this file then open the browser and type the URL: http://127.0.0.1:5000/ to use the web application

# Import relevant libraries
from flask import Flask, render_template, request, flash, session, redirect, url_for
import os
from compute import transcripts_roll_range, transcripts_all_range

# Initialize Flask object to create a web page and route to web pages
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "sample_input"
app.secret_key = "hello"

# Flask app routes the user to the index page of the web GUI
@app.route('/', methods=['GET', 'POST'])
def index():

	# Use POST method to fetch the information entered in the form
	if request.method == "POST":
		req = request.form

		# Fetch the range of roll numbers whose transcripts are to be generated
		roll = req.get("roll_range")

		# Create the input folder if it doesn't exist
		if not os.path.isdir(app.config['UPLOAD_FOLDER']):
			os.mkdir(app.config['UPLOAD_FOLDER'])

		# Save the files uploaded by user to sample_input folder 
		f1 = request.files["file1"]
		if f1.filename !='':
			f1.save(os.path.join(app.config['UPLOAD_FOLDER'], f1.filename))

		f2 = request.files["file2"]
		if f2.filename !='':
			f2.save(os.path.join(app.config['UPLOAD_FOLDER'], f2.filename))

		path1 = f1.filename
		path2 = f2.filename

		# Actions being performed when user clicks on the 2 buttons that are present in the GUI 
		if roll == "":

			if request.form["action"] == "Generate Transcripts for Given Roll Number":
				flash("Please enter the roll number range, eg: 0401CS10-0401CS15 ")

			elif request.form["action"] == "Generate all Transcripts":
				 result = transcripts_all_range(path1, path2)

			return redirect(request.url)

		else:

			if request.form["action"] == "Generate Transcripts for Given Roll Number":
				result = transcripts_roll_range(roll,path1, path2)

			else:
				result = None

		# Flash error messages to make sure program runs smoothly
		if result:
			flash(result)
			return redirect(request.url)

		# Redirects the user to the requested url
		return redirect(request.url)

	# Renders the main page of GUI
	return render_template('view.html')

if __name__ == '__main__':
	
	# Call the run function of flask app and enabling debugging in case of any errors
    app.run(debug=True)