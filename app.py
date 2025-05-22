from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Function to get city and state from pin code using an API
def get_location_details(pin_code):
    try:
        url = f"http://api.postalpincode.in/pincode/{pin_code}"  # Example API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad HTTP response codes
        data = response.json()
        
        if data[0]['Status'] == 'Success':
            city = data[0]['PostOffice'][0]['Division']
            state = data[0]['PostOffice'][0]['State']
            return city, state
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location details: {e}")
        return None, None

# Home route to display the enquiry form
@app.route('/')
def form():
    return render_template('form.html')

# Route to handle the form submission
@app.route('/submit-form', methods=['POST'])
def submit_form():
    full_name = request.form['fullName']
    mobile = request.form['mobile']
    email = request.form['email']
    pin_code = request.form['pinCode']
    city, state = get_location_details(pin_code)
    course = request.form['course']
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # You can store this data in a database or send it as an email, etc.
    # For now, we'll print it to the console (you can remove this line in production)
    print(f"Name: {full_name}, Mobile: {mobile}, Email: {email}, Pin Code: {pin_code}, City: {city}, State: {state}, Course: {course}, DateTime: {date_time}")

    # After form submission, redirect to the thank you page
    return render_template('thank_you.html', full_name=full_name)

# Route to get the city and state based on the pin code (AJAX call)
@app.route('/get-location')
def get_location():
    pin_code = request.args.get('pin_code')
    
    # Validate pin code before proceeding
    if pin_code and pin_code.isdigit():
        city, state = get_location_details(pin_code)
        if city and state:
            return jsonify({"city": city, "state": state})
        else:
            return jsonify({"city": None, "state": None})
    else:
        return jsonify({"city": None, "state": None})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Function to get city and state from pin code using an API
def get_location_details(pin_code):
    try:
        url = f"http://api.postalpincode.in/pincode/{pin_code}"  # Example API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad HTTP response codes
        data = response.json()
        
        if data[0]['Status'] == 'Success':
            city = data[0]['PostOffice'][0]['Division']
            state = data[0]['PostOffice'][0]['State']
            return city, state
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location details: {e}")
        return None, None

# Home route to display the enquiry form
@app.route('/')
def form():
    return render_template('form.html')

# Route to handle the form submission
@app.route('/submit-form', methods=['POST'])
def submit_form():
    full_name = request.form['fullName']
    mobile = request.form['mobile']
    email = request.form['email']
    pin_code = request.form['pinCode']
    city, state = get_location_details(pin_code)
    course = request.form['course']
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Logging submitted data (remove this in production)
    print(f"Name: {full_name}, Mobile: {mobile}, Email: {email}, Pin Code: {pin_code}, City: {city}, State: {state}, Course: {course}, DateTime: {date_time}")

    # Redirect to the thank you page
    return render_template('thank_you.html', full_name=full_name)

# Route to get the city and state based on the pin code (AJAX call)
@app.route('/get-location')
def get_location():
    pin_code = request.args.get('pin_code')
    
    # Validate pin code before proceeding
    if pin_code and pin_code.isdigit():
        city, state = get_location_details(pin_code)
        if city and state:
            return jsonify({"city": city, "state": state})
        else:
            return jsonify({"city": None, "state": None})
    else:
        return jsonify({"city": None, "state": None})

# Required for Vercel deployment
def handler(event, context):
    from flask import Request, Response
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)
