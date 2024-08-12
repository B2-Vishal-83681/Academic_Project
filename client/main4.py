from flask import Flask, render_template, request
import pickle
import datetime

# create an application of Flask
app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index4.html')


@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve form data
    product_category = request.form['product_category']
    product_price = float(request.form['product_price'])
    quantity = int(request.form['quantity'])
    total_purchase_amount = float(request.form['total_purchase_amount'])
    payment_method = request.form['payment_method']
    returns = int(request.form['returns'])
    age = int(request.form['age'])
    gender = request.form['gender']
    purchase_date = request.form['purchase_date']

    # Parse purchase date to get month, day, and day of the week
    purchase_date = datetime.datetime.strptime(purchase_date, "%Y-%m-%d")
    purchase_month = purchase_date.month
    purchase_day = purchase_date.day
    purchase_week = purchase_date.weekday()  # 0=Monday, 6=Sunday

    # Map categorical variables to numerical values
    product_category_mapping = {
        "Home": 3,
        "Electronics": 2,
        "Clothing": 1,
        "Books": 0
    }

    gender_mapping = {
        "Male": 1,
        "Female": 0
    }

    payment_method_mapping = {
        "Cash": 0,
        "Credit Card": 1,
        "Crypto": 2,
        "Paypal": 3
    }

    # Convert categorical values to numerical values
    product_category_value = product_category_mapping[product_category]
    gender_value = gender_mapping[gender]
    payment_method_value = payment_method_mapping[payment_method]

    # Load the model from model.pkl file
    with open('./model.pkl', 'rb') as file:
        model = pickle.load(file)

    # Make a prediction using the model
    prediction = model.predict([[
        product_category_value,
        product_price,
        quantity,
        total_purchase_amount,
        payment_method_value,
        returns,
        age,
        gender_value,
        purchase_month,
        purchase_day,
        purchase_week
    ]])

    # Determine prediction result
    result = 'Yes' if prediction[0] == 1 else 'No'
    print(f"prediction = {result}")

    # Render prediction result
    return render_template('index41.html', result=result)

# Start the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
