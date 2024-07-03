import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

app = Flask(__name__)
CORS(app)

# Global variable to store username
username = ""
password = ""

@app.route("/")
def home():
    return "home"

@app.route("/getformdata", methods=['POST'])
def getformdata():
    global username
    global password
    username = request.form['k1']
    password = request.form['k2']

    print(username)
    return "Data received"

@app.route("/getdata")
def getdata():
    global username  # Use global keyword to access the global variable
    global password
    if username:
        # Fetch only the 'username' field from Supabase based on the username
        response_username = supabase.table('users').select('username').execute()
        response_password = supabase.table('users').select('password').execute()
        data_username = response_username.data
        data_password = response_password.data
        if data_username:
            fetched_username = data_username[0]['username']
            fetched_password = data_password[0]['password']
            if fetched_username == username:
                if fetched_password == password:
                    return("Hello harsh")
                else:
                    return("passwords do not match")
            else:
                return("Email not found")
        else:
            return jsonify({"error": "No username found for the provided username"})
    else:
        return jsonify({"error": "No username provided"})

if __name__ == '__main__':
    app.run(debug=True)
