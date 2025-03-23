from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'db.db'

def analyze_data(database_path):
   '''

   This function contains Api endpoint linking which transfers the data we get from the user to our ML model

   We finished creating an API key to assign to our model and the web app, But we came across an issue,
   due to the lack of hosting resources from our end, We couldnt get a live web page which can be run through our 
   repository. We are providing you with the complete website and the model without the API integration.

   We tried everyway we can to integrate them so that it can work on your end, we tried GCP, Render, HuggingFace
   and even tried to run the model locally in a different file but still needed to host it on a cloud for
   it to be executable in our repository
   
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