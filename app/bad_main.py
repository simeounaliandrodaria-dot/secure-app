# This is an intentionally insecure web application

from flask import Flask, request

app = Flask(__name__)

# Insecure example: eval() function used to execute user input
@app.route('/eval', methods=['POST'])
def eval_input():
    user_input = request.form.get('input')
    return eval(user_input)

if __name__ == '__main__':
    app.run(debug=True)
