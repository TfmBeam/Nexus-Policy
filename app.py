from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

# Database configuration
DATABASE = 'db.db'

# Model function (replace with your actual ML model logic)
def analyze_data(database_path):
    """
    Placeholder for your ML model analysis.
    Replace this with your actual model's code.
    """
    try:
        conn = sqlite3.connect(database_path)
        df = pd.read_sql_query("SELECT * FROM data", conn)
        conn.close()

        # Example: Calculate the mean of a column (replace with your model's logic)
        if not df.empty and 'some_cloumn' in df.columns: #Add column check to avoid key errors.
            result = df['some_column'].mean()
        else:
            result = "No suitable data for analysis."

        return result

    except Exception as e:
        return f"Error during analysis: {e}"

def create_table(database_path, df):
    """Creates a table in the database from a pandas DataFrame."""
    try:
        conn = sqlite3.connect(database_path)
        df.to_sql('data', conn, if_exists='replace', index=False) # replace if the table 'data' already exists.
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
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
                if create_table(file, df):
                    return redirect(url_for('results'))
                else:
                    return "Error storing data in the database."

            except Exception as e:
                return f"Error processing CSV: {e}"

        else:
            return "Invalid file format. Please upload a CSV file."

    return render_template('import.html')

@app.route('/results')
def results():
    result = analyze_data(DATABASE)
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)