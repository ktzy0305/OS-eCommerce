# KT-Home
An ecommerce web application hosted using Flask with a MongoDB database.

## Setup
### 1. Clone this repository
```
git clone "https://github.com/ktzy0305/KT-Home.git"
```

### 2. Install all dependencies / packages
```
pip install -r requirements.txt
```

### 3. Set environment variables for flask
#### Unix based systems (Linux / MacOS)
```
export FLASK_APP=main.py
export FLASK_ENV=development
```
#### Windows based systems
```
set FLASK_APP=main.py
set FLASK_ENV=development
```
### 4. Start the application
```
flask run
```