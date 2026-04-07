from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Secure Flask Microservice"  # Add more security features as needed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # Set debug to False in production