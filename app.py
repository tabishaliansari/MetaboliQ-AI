from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary storage for user inputs
user_data = {}

@app.route('/')
def form_page_1():
    return render_template('form_page_1.html')

@app.route('/form_page_2', methods=['POST'])
def form_page_2():
    global user_data
    user_data.update(request.form.to_dict())  # Save data from Page 1
    return render_template('form_page_2.html')

@app.route('/result', methods=['POST'])
def result():
    global user_data
    user_data.update(request.form.to_dict())  # Save data from Page 2
    # Display collected data or perform prediction logic
    return render_template('result.html', data=user_data)

if __name__ == '__main__':
    app.run(debug=True)
