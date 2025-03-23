from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'db.db'

def analyze_data(database_path):
   '''

   This function contains Api endpoint linking which transfers the data we get from the user to our ML model

   Our Api endpoint linking is under development, Our model is completed and the link is provided in the repository.
   We are facing some issues while passing the data through the api url and the result that we're getting.
   We are experimenting with various cloud platforms to host our model.
   All hands are on deck for fixing this. We plan on resolving this very soon.
   
   '''

def create_table(database_path, df):
    '''
    This function takes the user csv data and creates a table to be inserted into our database using pandas.

    '''

    try:
        conn = sqlite3.connect(database_path)
        df.to_sql('data', conn, if_exists='replace', index=False)  
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False

@app.route('/import', methods=['GET', 'POST']) 
def import_data():
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            return redirect(request.url)

        file = request.files['csv_file']

        if file.filename == '':
            return redirect(request.url)

        if file and file.filename.endswith('.csv'):
            try:
                df = pd.read_csv(file)
                if create_table(DATABASE, df): 
                    return redirect(url_for('results'))
                else:
                    return "Error storing data in the database."

            except Exception as e:
                return f"Error processing CSV: {e}"

        else:
            return "Invalid file format. Please upload a CSV file."

    return render_template('file-selection.html') 

@app.route('/results')
def results():
    result = analyze_data(DATABASE) #This function is empty in the current version, the model can be accessed in our repository, We will display a static results table for presentation purpose
    return render_template('result.html', result=result)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)