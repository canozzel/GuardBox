import pyrebase

firebase_config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
    "databaseURL": "https://YOUR_PROJECT_ID.firebaseio.com",
    "storageBucket": "YOUR_PROJECT_ID.appspot.com"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
