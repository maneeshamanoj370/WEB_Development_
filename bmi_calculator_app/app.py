# bmi_calculator_app/app.py

from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

def calculate_bmi(height_cm, weight_kg):
    """
    Calculates the BMI, determines the category, and assigns a result color.
    Returns: bmi (float or None), category (str), color (str)
    """
    try:
        if height_cm <= 0 or weight_kg <= 0:
            raise ValueError("Height and weight must be positive.")

        # Convert height from cm to meters
        height_m = height_cm / 100.0
        
        # BMI formula: weight (kg) / [height (m)]^2
        bmi = weight_kg / (height_m ** 2)
        bmi = round(bmi, 1) # Round to one decimal place

        # Determine the BMI category and associated color
        if bmi < 18.5:
            category = "Underweight"
            color = "#007bff" # Blue
        elif 18.5 <= bmi < 24.9:
            category = "Normal"
            color = "#28a745" # Green
        elif 25.0 <= bmi < 29.9:
            category = "Overweight"
            color = "#ffc107" # Orange
        else: # bmi >= 30
            category = "Obese"
            color = "#dc3545" # Red
            
        return bmi, category, color
    
    except (ValueError, TypeError, ZeroDivisionError) as e:
        # Handle invalid inputs (non-numeric, zero, or negative)
        print(f"Error during calculation: {e}")
        return None, "Error: Invalid input. Enter positive numbers.", "#dc3545"

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles the BMI calculator form submission and display."""
    
    # Initialize variables for template
    bmi_result = None
    category_result = None
    color_code = None
    input_height = ""
    input_weight = ""

    if request.method == 'POST':
        try:
            # Safely get and convert form data
            height_cm = float(request.form.get('height'))
            weight_kg = float(request.form.get('weight'))

            # Keep input values to redisplay in the form fields
            input_height = height_cm
            input_weight = weight_kg
            
            # Calculate results
            bmi_result, category_result, color_code = calculate_bmi(height_cm, weight_kg)
            
        except ValueError:
            # This handles cases where conversion to float fails
            category_result = "Error: Please enter valid numeric values."
            color_code = "#dc3545"
            bmi_result = None

    # Render the HTML template, passing the results and input back
    return render_template(
        'index.html', 
        bmi=bmi_result, 
        category=category_result, 
        color=color_code,
        input_height=input_height,
        input_weight=input_weight
    )

if __name__ == '__main__':
    # Running on '0.0.0.0' allows access from local network devices (good for Linux hosting)
    # The default port is 5000
    app.run(host='0.0.0.0', debug=True)
